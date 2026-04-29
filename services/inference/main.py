from pathlib import Path
from time import time
from uuid import uuid4

import torch
import torch.nn as nn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_PATH = Path("ml/models/demo_model.pt")

app = FastAPI(title="Lumina Rec Inference API", version="0.1.0")


class PredictionRequest(BaseModel):
    features: list[float] = Field(..., min_length=10, max_length=10)


class PredictionResponse(BaseModel):
    prediction: float
    model_name: str
    model_version: str
    request_id: str
    latency_ms: float


def load_model() -> nn.Module:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

    model = nn.Linear(10, 1)
    state_dict = torch.load(MODEL_PATH, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model


model = load_model()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    return {"status": "ready"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    request_id = str(uuid4())
    start_time = time()

    try:
        x = torch.tensor([request.features], dtype=torch.float32)

        with torch.no_grad():
            prediction = model(x).item()

        latency_ms = round((time() - start_time) * 1000, 2)

        return PredictionResponse(
            prediction=prediction,
            model_name="lumina-rec-demo-model",
            model_version="0.1.0",
            request_id=request_id,
            latency_ms=latency_ms,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))