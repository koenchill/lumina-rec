from pathlib import Path

import torch
import torch.nn as nn
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_PATH = Path("ml/models/demo_model.pt")

app = FastAPI(title="Lumina Rec Inference API", version="0.1.0")


class PredictionRequest(BaseModel):
    features: list[float] = Field(..., min_length=10, max_length=10)


class PredictionResponse(BaseModel):
    prediction: float


def load_model() -> nn.Module:
    model = nn.Linear(10, 1)
    state_dict = torch.load(MODEL_PATH, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model


model = load_model()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    x = torch.tensor([request.features], dtype=torch.float32)

    with torch.no_grad():
        prediction = model(x).item()

    return PredictionResponse(prediction=prediction)