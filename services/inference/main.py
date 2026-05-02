import hashlib
import json
import logging
import os
from pathlib import Path
from time import time
from uuid import uuid4

import mlflow
import pandas as pd
import torch
import torch.nn as nn
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import Response
from mlflow.tracking import MlflowClient
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

load_dotenv()

MODEL_RUN_ID = os.getenv("MODEL_RUN_ID")
MODEL_ARTIFACT_PATH = os.getenv("MODEL_ARTIFACT_PATH", "approved_model")
MODEL_SHA256 = os.getenv("MODEL_SHA256")

USE_MODEL_REGISTRY = os.getenv("USE_MODEL_REGISTRY", "false").lower() == "true"
REGISTERED_MODEL_NAME = os.getenv("REGISTERED_MODEL_NAME", "lumina-rec-movielens-mf")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "approved")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
APPROVED_MODEL_DIR = Path(os.getenv("APPROVED_MODEL_DIR", "ml/models/approved"))

API_KEY = os.getenv("LUMINA_API_KEY", "local-dev-api-key")
RATE_LIMIT = os.getenv("LUMINA_RATE_LIMIT", "30/minute")

DEFAULT_MODEL_NAME = "lumina-rec-movielens-mf"
DEFAULT_MODEL_VERSION = "0.2.0"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("lumina-rec-inference")

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Lumina Rec Inference API", version=DEFAULT_MODEL_VERSION)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

PREDICTION_REQUESTS = Counter(
    "lumina_prediction_requests_total",
    "Total number of prediction and recommendation requests",
)

PREDICTION_ERRORS = Counter(
    "lumina_prediction_errors_total",
    "Total number of failed prediction and recommendation requests",
)

PREDICTION_LATENCY = Histogram(
    "lumina_prediction_latency_ms",
    "Prediction and recommendation latency in milliseconds",
)

RATE_LIMIT_ERRORS = Counter(
    "lumina_rate_limit_errors_total",
    "Total number of rate limited requests",
)


class MatrixFactorizationModel(nn.Module):
    def __init__(self, num_users: int, num_movies: int, embedding_dim: int):
        super().__init__()

        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.movie_embedding = nn.Embedding(num_movies, embedding_dim)
        self.user_bias = nn.Embedding(num_users, 1)
        self.movie_bias = nn.Embedding(num_movies, 1)
        self.global_bias = nn.Parameter(torch.zeros(1))

    def forward(self, user_idx: torch.Tensor, movie_idx: torch.Tensor) -> torch.Tensor:
        user_vector = self.user_embedding(user_idx)
        movie_vector = self.movie_embedding(movie_idx)

        dot_product = (user_vector * movie_vector).sum(dim=1)
        user_bias = self.user_bias(user_idx).squeeze()
        movie_bias = self.movie_bias(movie_idx).squeeze()

        rating = dot_product + user_bias + movie_bias + self.global_bias
        return torch.clamp(rating, min=0.5, max=5.0)


class PredictionRequest(BaseModel):
    user_id: int = Field(..., description="MovieLens userId")
    movie_id: int = Field(..., description="MovieLens movieId")


class PredictionResponse(BaseModel):
    predicted_rating: float
    user_id: int
    movie_id: int
    model_name: str
    model_version: str
    request_id: str
    latency_ms: float


class RecommendationRequest(BaseModel):
    user_id: int = Field(..., description="MovieLens userId")
    top_n: int = Field(default=10, ge=1, le=50)


class RecommendationItem(BaseModel):
    movie_id: int
    title: str
    genres: str
    predicted_rating: float


class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: list[RecommendationItem]
    model_name: str
    model_version: str
    request_id: str
    latency_ms: float


class MovieMetadataResponse(BaseModel):
    movie_id: int
    title: str
    genres: str


def log_event(event_name: str, **fields) -> None:
    log_record = {"event": event_name, **fields}
    logger.info(json.dumps(log_record))


def calculate_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


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
        content={"detail": "Rate limit exceeded"},
    )


def verify_api_key(x_api_key: str | None) -> None:
    if not x_api_key or x_api_key != API_KEY:
        log_event("authentication_failed", status="error")
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


def resolve_model_run_id() -> str:
    if MODEL_RUN_ID:
        return MODEL_RUN_ID

    if not USE_MODEL_REGISTRY:
        raise ValueError("MODEL_RUN_ID is required unless USE_MODEL_REGISTRY=true")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

    model_version = client.get_model_version_by_alias(
        name=REGISTERED_MODEL_NAME,
        alias=MODEL_ALIAS,
    )

    if not model_version.run_id:
        raise ValueError(
            f"No run ID found for model alias: {REGISTERED_MODEL_NAME}@{MODEL_ALIAS}"
        )

    return model_version.run_id


def download_approved_artifacts() -> tuple[Path, str]:
    resolved_run_id = resolve_model_run_id()

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    APPROVED_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    artifact_local_path = mlflow.artifacts.download_artifacts(
        run_id=resolved_run_id,
        artifact_path=MODEL_ARTIFACT_PATH,
        dst_path=str(APPROVED_MODEL_DIR),
    )

    return Path(artifact_local_path), resolved_run_id


def load_json(file_path: Path) -> dict:
    return json.loads(file_path.read_text(encoding="utf-8"))


def load_movies_metadata(file_path: Path) -> dict[int, dict[str, str]]:
    movies_metadata_df = pd.read_csv(file_path)

    return {
        int(row["movieId"]): {
            "title": str(row["title"]),
            "genres": str(row["genres"]),
        }
        for _, row in movies_metadata_df.iterrows()
    }


def get_model_name() -> str:
    return model_metadata.get("model_name", DEFAULT_MODEL_NAME)


def get_model_version() -> str:
    return model_metadata.get("model_version", DEFAULT_MODEL_VERSION)


def get_resolved_model_run_id() -> str:
    return model_metadata.get("resolved_model_run_id", str(MODEL_RUN_ID))


def load_model() -> tuple[nn.Module, dict, dict, dict[int, dict[str, str]], str]:
    artifact_dir, resolved_run_id = download_approved_artifacts()

    model_path = artifact_dir / "recommender_model.pt"
    metadata_path = artifact_dir / "model_metadata.json"
    mappings_path = artifact_dir / "movielens_mappings.json"
    movies_metadata_path = artifact_dir / "movies_metadata.csv"

    if not model_path.exists():
        raise FileNotFoundError(f"Approved model file not found: {model_path}")

    if not metadata_path.exists():
        raise FileNotFoundError(f"Model metadata file not found: {metadata_path}")

    if not mappings_path.exists():
        raise FileNotFoundError(f"MovieLens mappings file not found: {mappings_path}")

    if not movies_metadata_path.exists():
        raise FileNotFoundError(f"Movie metadata file not found: {movies_metadata_path}")

    actual_sha256 = calculate_sha256(model_path)

    if MODEL_SHA256 and actual_sha256 != MODEL_SHA256:
        log_event(
            "model_checksum_failed",
            model_path=str(model_path),
            expected_sha256=MODEL_SHA256,
            actual_sha256=actual_sha256,
            status="error",
        )
        raise ValueError("Model checksum validation failed")

    metadata = load_json(metadata_path)
    mappings = load_json(mappings_path)
    movies_metadata = load_movies_metadata(movies_metadata_path)
    metadata["resolved_model_run_id"] = resolved_run_id

    model_payload = torch.load(
        model_path,
        map_location="cpu",
        weights_only=False,
    )

    loaded_model = MatrixFactorizationModel(
        num_users=int(model_payload["num_users"]),
        num_movies=int(model_payload["num_movies"]),
        embedding_dim=int(model_payload["embedding_dim"]),
    )

    loaded_model.load_state_dict(model_payload["state_dict"])
    loaded_model.eval()

    log_event(
        "model_loaded",
        model_name=metadata.get("model_name", DEFAULT_MODEL_NAME),
        model_version=metadata.get("model_version", DEFAULT_MODEL_VERSION),
        model_path=str(model_path),
        model_run_id=resolved_run_id,
        artifact_path=MODEL_ARTIFACT_PATH,
        model_sha256=actual_sha256,
        checksum_validation="enabled" if MODEL_SHA256 else "not_configured",
        model_registry_enabled=str(USE_MODEL_REGISTRY).lower(),
        registered_model_name=REGISTERED_MODEL_NAME,
        model_alias=MODEL_ALIAS,
        movie_metadata_count=len(movies_metadata),
    )

    return loaded_model, metadata, mappings, movies_metadata, actual_sha256


model, model_metadata, model_mappings, movies_metadata, model_actual_sha256 = load_model()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

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
    }


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/movies/{movie_id}", response_model=MovieMetadataResponse)
def get_movie(movie_id: int) -> MovieMetadataResponse:
    metadata = movies_metadata.get(movie_id)

    if not metadata:
        raise HTTPException(
            status_code=404,
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
        verify_api_key(x_api_key)

        user_key = str(prediction_request.user_id)
        movie_key = str(prediction_request.movie_id)

        user_to_idx = model_mappings["user_to_idx"]
        movie_to_idx = model_mappings["movie_to_idx"]

        if user_key not in user_to_idx:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown user_id: {prediction_request.user_id}",
            )

        if movie_key not in movie_to_idx:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown movie_id: {prediction_request.movie_id}",
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

        raise HTTPException(status_code=500, detail="Prediction failed")


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
        verify_api_key(x_api_key)

        user_key = str(recommendation_request.user_id)

        user_to_idx = model_mappings["user_to_idx"]
        idx_to_movie = model_mappings["idx_to_movie"]

        if user_key not in user_to_idx:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown user_id: {recommendation_request.user_id}",
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

        top_items = ranked[: recommendation_request.top_n]

        recommendations = []

        for movie_idx, score in top_items:
            movie_id = int(idx_to_movie[str(movie_idx)])
            metadata = movies_metadata.get(
                movie_id,
                {
                    "title": "Unknown title",
                    "genres": "Unknown",
                },
            )

            recommendations.append(
                RecommendationItem(
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
            latency_ms=latency_ms,
            status="success",
        )

        return RecommendationResponse(
            user_id=recommendation_request.user_id,
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

        raise HTTPException(status_code=500, detail="Recommendation failed")