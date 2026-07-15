import logging
from time import time
from uuid import uuid4

import torch
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from services.inference.app.auth import raise_api_error, verify_api_key
from services.inference.app.config import (
    DEFAULT_MODEL_NAME,
    DEFAULT_MODEL_VERSION,
    MODEL_ALIAS,
    MODEL_ARTIFACT_PATH,
    MODEL_RUN_ID,
    MODEL_SHA256,
    RATE_LIMIT,
    REGISTERED_MODEL_NAME,
    USE_MODEL_REGISTRY,
)
from services.inference.app.loading import load_model
from services.inference.app.logging_utils import log_event
from services.inference.app.metrics import (
    PREDICTION_ERRORS,
    PREDICTION_LATENCY,
    PREDICTION_REQUESTS,
    RATE_LIMIT_ERRORS,
)
from services.inference.app.schemas import (
    ModelInfoResponse,
    MovieMetadataResponse,
    PredictionRequest,
    PredictionResponse,
    RecommendationItem,
    RecommendationRequest,
    RecommendationResponse,
    VersionResponse,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Lumina Rec Inference API", version=DEFAULT_MODEL_VERSION)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

model, model_metadata, model_mappings, movies_metadata, model_actual_sha256 = load_model()


def get_model_name() -> str:
    return model_metadata.get("model_name", DEFAULT_MODEL_NAME)


def get_model_version() -> str:
    return model_metadata.get("model_version", DEFAULT_MODEL_VERSION)


def get_resolved_model_run_id() -> str:
    return model_metadata.get("resolved_model_run_id", str(MODEL_RUN_ID))


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    RATE_LIMIT_ERRORS.inc()

    log_event(
        "rate_limit_exceeded",
        client=get_remote_address(request),
        status="error",
    )

    return JSONResponse(
        status_code=429,
        content={
            "detail": {
                "error_code": "RATE_LIMIT_EXCEEDED",
                "detail": "Rate limit exceeded",
                "request_id": None,
            }
        },
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    if model is None:
        raise_api_error(
            status_code=503,
            error_code="MODEL_NOT_LOADED",
            detail="Model is not loaded",
        )

    return {
        "status": "ready",
        "model_name": get_model_name(),
        "model_version": get_model_version(),
        "model_run_id": get_resolved_model_run_id(),
        "model_artifact_path": MODEL_ARTIFACT_PATH,
        "model_sha256": model_actual_sha256,
        "checksum_validation": "enabled" if MODEL_SHA256 else "not_configured",
        "model_registry_enabled": str(USE_MODEL_REGISTRY).lower(),
        "registered_model_name": REGISTERED_MODEL_NAME,
        "model_alias": MODEL_ALIAS,
        "movie_metadata_status": "loaded",
        "movie_metadata_count": str(len(movies_metadata)),
        "artifact_manifest_status": model_metadata.get(
            "artifact_manifest_status",
            "not_validated",
        ),
        "artifact_manifest_version": model_metadata.get(
            "artifact_manifest_version",
            "unknown",
        ),
    }


@app.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    return VersionResponse(
        service_name="lumina-rec-inference",
        service_version=DEFAULT_MODEL_VERSION,
        model_name=get_model_name(),
        model_version=get_model_version(),
    )


@app.get("/model", response_model=ModelInfoResponse)
def model_info() -> ModelInfoResponse:
    return ModelInfoResponse(
        model_name=get_model_name(),
        model_version=get_model_version(),
        model_run_id=get_resolved_model_run_id(),
        model_artifact_path=MODEL_ARTIFACT_PATH,
        model_sha256=model_actual_sha256,
        checksum_validation="enabled" if MODEL_SHA256 else "not_configured",
        artifact_manifest_status=model_metadata.get(
            "artifact_manifest_status",
            "not_validated",
        ),
        artifact_manifest_version=model_metadata.get(
            "artifact_manifest_version",
            "unknown",
        ),
        model_registry_enabled=str(USE_MODEL_REGISTRY).lower(),
        registered_model_name=REGISTERED_MODEL_NAME,
        model_alias=MODEL_ALIAS,
    )


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/movies/{movie_id}", response_model=MovieMetadataResponse)
def get_movie(movie_id: int) -> MovieMetadataResponse:
    metadata = movies_metadata.get(movie_id)

    if not metadata:
        raise_api_error(
            status_code=404,
            error_code="UNKNOWN_MOVIE_ID",
            detail=f"Unknown movie_id: {movie_id}",
        )

    return MovieMetadataResponse(
        movie_id=movie_id,
        title=metadata["title"],
        genres=metadata["genres"],
    )


@app.post("/predict", response_model=PredictionResponse)
@limiter.limit(RATE_LIMIT)
def predict(
    request: Request,
    prediction_request: PredictionRequest,
    x_api_key: str | None = Header(default=None),
) -> PredictionResponse:
    request_id = str(uuid4())
    start_time = time()

    try:
        verify_api_key(x_api_key, request_id=request_id)

        user_key = str(prediction_request.user_id)
        movie_key = str(prediction_request.movie_id)

        user_to_idx = model_mappings["user_to_idx"]
        movie_to_idx = model_mappings["movie_to_idx"]

        if user_key not in user_to_idx:
            raise_api_error(
                status_code=404,
                error_code="UNKNOWN_USER_ID",
                detail=f"Unknown user_id: {prediction_request.user_id}",
                request_id=request_id,
            )

        if movie_key not in movie_to_idx:
            raise_api_error(
                status_code=404,
                error_code="UNKNOWN_MOVIE_ID",
                detail=f"Unknown movie_id: {prediction_request.movie_id}",
                request_id=request_id,
            )

        user_idx = torch.tensor([int(user_to_idx[user_key])], dtype=torch.long)
        movie_idx = torch.tensor([int(movie_to_idx[movie_key])], dtype=torch.long)

        with torch.no_grad():
            predicted_rating = float(model(user_idx, movie_idx).item())

        latency_ms = round((time() - start_time) * 1000, 2)

        PREDICTION_REQUESTS.inc()
        PREDICTION_LATENCY.observe(latency_ms)

        log_event(
            "prediction_completed",
            request_id=request_id,
            model_name=get_model_name(),
            model_version=get_model_version(),
            model_run_id=get_resolved_model_run_id(),
            user_id=prediction_request.user_id,
            movie_id=prediction_request.movie_id,
            latency_ms=latency_ms,
            status="success",
        )

        return PredictionResponse(
            predicted_rating=round(predicted_rating, 4),
            user_id=prediction_request.user_id,
            movie_id=prediction_request.movie_id,
            model_name=get_model_name(),
            model_version=get_model_version(),
            request_id=request_id,
            latency_ms=latency_ms,
        )

    except HTTPException:
        PREDICTION_ERRORS.inc()
        raise

    except Exception as exc:
        latency_ms = round((time() - start_time) * 1000, 2)
        PREDICTION_ERRORS.inc()

        log_event(
            "prediction_failed",
            request_id=request_id,
            model_name=get_model_name(),
            model_version=get_model_version(),
            model_run_id=get_resolved_model_run_id(),
            latency_ms=latency_ms,
            status="error",
            error=str(exc),
        )

        raise_api_error(
            status_code=500,
            error_code="PREDICTION_FAILED",
            detail="Prediction failed",
            request_id=request_id,
        )


@app.post("/recommend", response_model=RecommendationResponse)
@limiter.limit(RATE_LIMIT)
def recommend(
    request: Request,
    recommendation_request: RecommendationRequest,
    x_api_key: str | None = Header(default=None),
) -> RecommendationResponse:
    request_id = str(uuid4())
    start_time = time()

    try:
        verify_api_key(x_api_key, request_id=request_id)

        user_key = str(recommendation_request.user_id)

        user_to_idx = model_mappings["user_to_idx"]
        idx_to_movie = model_mappings["idx_to_movie"]

        if user_key not in user_to_idx:
            raise_api_error(
                status_code=404,
                error_code="UNKNOWN_USER_ID",
                detail=f"Unknown user_id: {recommendation_request.user_id}",
                request_id=request_id,
            )

        user_idx_value = int(user_to_idx[user_key])
        movie_indices = [int(index) for index in idx_to_movie.keys()]

        user_tensor = torch.tensor(
            [user_idx_value] * len(movie_indices),
            dtype=torch.long,
        )
        movie_tensor = torch.tensor(movie_indices, dtype=torch.long)

        with torch.no_grad():
            predictions = model(user_tensor, movie_tensor).tolist()

        ranked = sorted(
            zip(movie_indices, predictions),
            key=lambda item: item[1],
            reverse=True,
        )

        filtered_items = []

        for movie_idx, score in ranked:
            movie_id = int(idx_to_movie[str(movie_idx)])
            metadata = movies_metadata.get(
                movie_id,
                {
                    "title": "Unknown title",
                    "genres": "Unknown",
                },
            )

            if recommendation_request.genre:
                requested_genre = recommendation_request.genre.lower()
                movie_genres = metadata["genres"].lower().split("|")

                if requested_genre not in movie_genres:
                    continue

            filtered_items.append((movie_idx, score, metadata))

            if len(filtered_items) == recommendation_request.top_n:
                break

        recommendations = []

        for rank, (movie_idx, score, metadata) in enumerate(filtered_items, start=1):
            movie_id = int(idx_to_movie[str(movie_idx)])

            recommendations.append(
                RecommendationItem(
                    rank=rank,
                    movie_id=movie_id,
                    title=metadata["title"],
                    genres=metadata["genres"],
                    predicted_rating=round(float(score), 4),
                )
            )

        latency_ms = round((time() - start_time) * 1000, 2)

        PREDICTION_REQUESTS.inc()
        PREDICTION_LATENCY.observe(latency_ms)

        log_event(
            "recommendation_completed",
            request_id=request_id,
            model_name=get_model_name(),
            model_version=get_model_version(),
            model_run_id=get_resolved_model_run_id(),
            user_id=recommendation_request.user_id,
            top_n=recommendation_request.top_n,
            returned_count=len(recommendations),
            genre=recommendation_request.genre,
            latency_ms=latency_ms,
            status="success",
        )

        return RecommendationResponse(
            user_id=recommendation_request.user_id,
            top_n=recommendation_request.top_n,
            returned_count=len(recommendations),
            genre=recommendation_request.genre,
            recommendations=recommendations,
            model_name=get_model_name(),
            model_version=get_model_version(),
            request_id=request_id,
            latency_ms=latency_ms,
        )

    except HTTPException:
        PREDICTION_ERRORS.inc()
        raise

    except Exception as exc:
        latency_ms = round((time() - start_time) * 1000, 2)
        PREDICTION_ERRORS.inc()

        log_event(
            "recommendation_failed",
            request_id=request_id,
            model_name=get_model_name(),
            model_version=get_model_version(),
            model_run_id=get_resolved_model_run_id(),
            user_id=recommendation_request.user_id,
            latency_ms=latency_ms,
            status="error",
            error=str(exc),
        )

        raise_api_error(
            status_code=500,
            error_code="RECOMMENDATION_FAILED",
            detail="Recommendation failed",
            request_id=request_id,
        )
