import json
import logging
from pathlib import Path
from time import time
from uuid import uuid4

import torch
import torch.nn as nn
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, Field

MODEL_NAME = "lumina-rec-demo-model"
MODEL_VERSION = "0.1.0"
MODEL_PATH = Path("ml/models/demo_model.pt")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("lumina-rec-inference")

app = FastAPI(title="Lumina Rec Inference API", version=MODEL_VERSION)

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


def load_model() -> nn.Module:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

    model = nn.Linear(10, 1)
    state_dict = torch.load(MODEL_PATH, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()

    log_event(
        "model_loaded",
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        model_path=str(MODEL_PATH),
    )

    return model


model = load_model()


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
    }


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    request_id = str(uuid4())
    start_time = time()

    try:
        x = torch.tensor([request.features], dtype=torch.float32)

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