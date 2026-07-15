# Lumina Rec Reviewer Guide

## Purpose

This guide helps a reviewer validate the Lumina Rec local MLOps stack quickly.

## What This Project Shows

Lumina Rec demonstrates a local production shaped MLOps backend with:

- MovieLens matrix factorization model training
- MLflow tracking
- MinIO artifact storage
- Postgres metadata storage
- FastAPI inference
- API key authentication
- Rate limiting
- Model checksum validation
- Approved model loading by MLflow run ID
- Prometheus metrics
- Structured logs
- Docker Compose orchestration
- Automated tests
- Load testing
- CI security checks

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

## Start Here

Read these files first:

| File | Why It Matters |
|---|---|
| README.md | Project overview and common commands |
| [docs/architecture/architecture.md](../architecture/architecture.md) | Architecture diagram and service flow |
| [docs/api/api_contract.md](../api/api_contract.md) | API endpoints and expected responses |
| [docs/api/recommendation_api.md](../api/recommendation_api.md) | Prediction and recommendation API details |
| [docs/mlops/model_card.md](../mlops/model_card.md) | Approved model details and limitations |
| [docs/mlops/model_promotion_record.md](../mlops/model_promotion_record.md) | Promotion decision and approved run |
| [docs/operations/local_validation.md](../operations/local_validation.md) | Evidence the stack works |
| [docs/security/security_controls.md](../security/security_controls.md) | Implemented controls and risk reduction |
| [docs/security/threat_model.md](../security/threat_model.md) | Security risks and planned controls |

## Quick Validation

Run:

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 movie
```

Expected result:

- `/ready` returns approved model metadata and checksum status
- `/predict` returns a rating prediction
- `/recommend` returns a top N recommendation list
- API tests pass
- `/movies/{movie_id}` returns movie title and genre metadata
- `/movies/{movie_id}` returns movie title and genre metadata
## Docker Validation

Run:

```powershell
docker compose ps
```

Expected core services:

- inference
- mlflow
- postgres
- minio

## Security Validation

Check:

- `/predict` requires `x-api-key`
- `/recommend` requires `x-api-key`
- `.env` is not committed
- model checksum validation is enabled
- inference loads artifacts from MLflow by run ID
- CI includes Gitleaks and Trivy
- API tests validate authentication failures
- metrics include request, error, latency, and rate limit counters

## Load Test

Run:

```powershell
.\scripts\lumina.ps1 load-test
```

Expected result:

- 0 failures
- Predict median latency near the current local baseline
- Report generated at `tests/load/load_test_report.html`

Do not commit the generated HTML report.

## Current Known Limitation

The model is still a baseline matrix factorization model.

Next major engineering improvements:

- Add movie title and genre metadata to recommendation responses
- Add MLflow Model Registry alias for approved model selection
- Add dataset checksum validation
- Add a production deployment path