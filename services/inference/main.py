import hashlib
import json
import logging
import os
from pathlib import Path
from time import time
from uuid import uuid4

import torch
import torch.nn as nn
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

load_dotenv()

MODEL_NAME = "lumina-rec-demo-model"
MODEL_VERSION = "0.1.0"
MODEL_PATH = Path(os.getenv("MODEL_PATH", "ml/models/demo_model.pt"))
MODEL_SHA256 = os.getenv("MODEL_SHA256")
API_KEY = os.getenv("LUMINA_API_KEY", "local-dev-api-key")
RATE_LIMIT = os.getenv("LUMINA_RATE_LIMIT", "30/minute")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("lumina-rec-inference")

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Lumina Rec Inference API", version=MODEL_VERSION)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

PREDICTION_REQUESTS = Counter(
    "lumina_prediction_requests_total",
    "Total number of prediction requests",
)

PREDICTION_ERRORS = Counter(
    "lumina_prediction_errors_total",
    "Total number of failed prediction requests",
)

PREDICTION_LATENCY = Histogram(
    "lumina_prediction_latency_ms",
    "Prediction latency in milliseconds",
)

RATE_LIMIT_ERRORS = Counter(
    "lumina_rate_limit_errors_total",
    "Total number of rate limited requests",
)


class PredictionRequest(BaseModel):
    features: list[float] = Field(..., min_length=10, max_length=10)


class PredictionResponse(BaseModel):
    prediction: float
    model_name: str
    model_version: str
    request_id: str
    latency_ms: float


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


def load_model() -> tuple[nn.Module, str]:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

    actual_sha256 = calculate_sha256(MODEL_PATH)

    if MODEL_SHA256 and actual_sha256 != MODEL_SHA256:
        log_event(
            "model_checksum_failed",
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
            model_path=str(MODEL_PATH),
            expected_sha256=MODEL_SHA256,
            actual_sha256=actual_sha256,
            status="error",
        )
        raise ValueError("Model checksum validation failed")

    model = nn.Linear(10, 1)
    state_dict = torch.load(MODEL_PATH, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()

    log_event(
        "model_loaded",
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        model_path=str(MODEL_PATH),
        model_sha256=actual_sha256,
        checksum_validation="enabled" if MODEL_SHA256 else "not_configured",
    )

    return model, actual_sha256


model, model_actual_sha256 = load_model()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    return {
        "status": "ready",
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "model_sha256": model_actual_sha256,
        "checksum_validation": "enabled" if MODEL_SHA256 else "not_configured",
    }


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


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

        x = torch.tensor([prediction_request.features], dtype=torch.float32)

        with torch.no_grad():
            prediction = model(x).item()

        latency_ms = round((time() - start_time) * 1000, 2)

        PREDICTION_REQUESTS.inc()
        PREDICTION_LATENCY.observe(latency_ms)

        log_event(
            "prediction_completed",
            request_id=request_id,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
            latency_ms=latency_ms,
            status="success",
        )

        return PredictionResponse(
            prediction=prediction,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
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
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
            latency_ms=latency_ms,
            status="error",
            error=str(exc),
        )

        raise HTTPException(status_code=500, detail="Prediction failed")