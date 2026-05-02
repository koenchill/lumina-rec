# Inference Service

## Purpose

This service hosts the Lumina Rec FastAPI inference API.

## Endpoints

| Endpoint | Purpose |
|---|---|
| GET /health | Health check |
| GET /ready | Model readiness check |
| GET /metrics | Prometheus metrics |
| GET /movies/{movie_id} | Movie metadata lookup |
| POST /predict | Predict rating for one user and movie |
| POST /recommend | Return top N recommendations |

## Runtime Dependencies

The service loads approved model artifacts from MLflow.

Required artifacts:

| Artifact | Purpose |
|---|---|
| recommender_model.pt | PyTorch model |
| model_metadata.json | Model metadata |
| movielens_mappings.json | User and movie mappings |
| movies_metadata.csv | Movie title and genre metadata |

## Local Validation

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 test