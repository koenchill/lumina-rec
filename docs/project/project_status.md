# Lumina Rec Project Status

## Date

April 30, 2026

## Current Status

The local Lumina Rec MLOps stack now serves a real MovieLens recommendation model.

The project has moved beyond the original demo model. It now trains a PyTorch matrix factorization model, logs approved artifacts to MLflow, loads the approved model into FastAPI by MLflow run ID, validates the model checksum, and serves both rating predictions and top N recommendations.

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| Dataset | MovieLens latest small |
| Model type | Matrix factorization |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Completed

- Created local Docker Compose stack
- Added MLflow tracking server
- Added Postgres backend store
- Added MinIO artifact store
- Created MinIO `mlflow-artifacts` bucket
- Added FastAPI inference service
- Replaced demo model with MovieLens matrix factorization model
- Logged model training run to MLflow
- Logged approved model artifacts to MLflow
- Added approved model loading by `MODEL_RUN_ID`
- Added SHA256 model checksum validation
- Added `/predict` endpoint for rating prediction
- Added `/recommend` endpoint for top N recommendations
- Added API key authentication
- Added configurable rate limiting
- Added Prometheus metrics
- Added structured JSON logs
- Added readiness and health endpoints
- Added PowerShell task runner
- Added pytest inference API tests
- Added Locust load test
- Added GitHub Actions CI
- Added secret scanning
- Added container vulnerability scanning
- Added API contract
- Added threat model
- Added security controls document
- Added incident response runbook
- Added model rollback procedure
- Added model promotion record
- Added recommendation API documentation
- Added model card
- Added data dictionary
- Added repository structure documentation
- Added `/movies/{movie_id}` endpoint for movie title and genre lookup
- Added `/movies/{movie_id}` endpoint for movie title and genre lookup

## Current Working Commands

```powershell
.\scripts\lumina.ps1 up
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 load-test
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 movie
```

## Current Local URLs

| Service | URL |
|---|---|
| Inference API | http://localhost:8001 |
| MLflow | http://localhost:5000 |
| MinIO | http://localhost:9001 |
| Keycloak | http://localhost:8082 |
| LocalStack | http://localhost:4566 |

## Required Local Environment Values

```env
MODEL_RUN_ID=14eda4cf03bd4d328a3ee791ec9a002f
MODEL_SHA256=205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd
MODEL_ARTIFACT_PATH=approved_model
```

## Known Rules

- Do not commit `.env`.
- Do not commit `ml/models/approved/`.
- Do not commit `tests/load/load_test_report.html`.
- Do not promote a new model unless RMSE improves or there is a clear test reason.
- If a new model is promoted, update `MODEL_RUN_ID` and `MODEL_SHA256`.
- If inference does not become ready, check `docker compose logs inference --tail=120`.
- Use `scripts\lumina.ps1` instead of `make` on Windows.

## Next Work Session

Recommended next steps:

1. Add movie title and genre metadata to recommendation responses.
2. Add `/movies/{movie_id}` lookup endpoint.
3. Add MLflow Model Registry alias or stage for approved models.
4. Add dataset checksum validation.
5. Add model performance promotion gate.
6. Update CI to test `/recommend`.
7. Add Grafana dashboard for inference metrics.
8. Add production deployment path.