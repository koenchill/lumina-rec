# Lumina Rec Deployment Notes

## Purpose

This document captures deployment decisions for the local Lumina Rec MLOps stack.

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Local Deployment Pattern

Lumina Rec runs locally with Docker Compose.

Core services:

| Service | Purpose |
|---|---|
| inference | FastAPI inference API |
| mlflow | MLflow tracking server |
| minio | S3 compatible artifact storage |
| postgres | MLflow backend metadata store |
| redis | Future cache placeholder |
| keycloak | Future identity provider placeholder |
| localstack | Future AWS local development placeholder |

## Inference Container

The inference image uses:

```text
python:3.11-slim
```

The inference container installs CPU only PyTorch.

CPU only PyTorch is used because the local model is small and does not require GPU acceleration.

## Why CPU Only PyTorch

CPU only PyTorch reduces:

- Docker image size
- Build time
- Network download failures
- Unnecessary CUDA package downloads
- Local machine resource usage

## Required Runtime Values

The inference service requires:

```env
MODEL_RUN_ID=14eda4cf03bd4d328a3ee791ec9a002f
MODEL_SHA256=205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd
MODEL_ARTIFACT_PATH=approved_model
```

Inside Docker Compose, inference must use Docker service names:

```env
MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_S3_ENDPOINT_URL=http://minio:9000
```

On the Windows host, training uses localhost:

```env
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_S3_ENDPOINT_URL=http://localhost:9000
```

## Start Required Services

```powershell
docker compose up -d postgres minio mlflow
```

## Confirm MLflow

```powershell
Invoke-WebRequest -Uri http://localhost:5000 -UseBasicParsing
```

Expected:

```text
StatusCode : 200
```

## Confirm MinIO Bucket

```powershell
docker compose exec minio mc ls local
```

Expected bucket:

```text
mlflow-artifacts
```

Create bucket if missing:

```powershell
docker compose exec minio mc alias set local http://localhost:9000 minio minio123
docker compose exec minio mc mb local/mlflow-artifacts
```

## Build Inference

```powershell
docker compose up -d --build inference
```

## Validate Inference

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test
```

## Expected Readiness

```json
{
  "status": "ready",
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0",
  "model_run_id": "14eda4cf03bd4d328a3ee791ec9a002f",
  "model_artifact_path": "approved_model",
  "model_sha256": "205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd",
  "checksum_validation": "enabled"
}
```

## Supported API Workflows

| Endpoint | Purpose |
|---|---|
| GET /health | Confirms service is running |
| GET /ready | Confirms approved model is loaded |
| GET /metrics | Exposes Prometheus metrics |
| POST /predict | Predicts rating for one user and movie |
| POST /recommend | Returns top N movie recommendations |

## Files Not To Commit

```text
.env
.venv/
ml/models/approved/
ml/models/*.pt
tests/load/load_test_report.html
__pycache__/
*.pyc
```

## Production Deployment Notes

For production, replace local patterns with:

- Managed MLflow or model registry
- Managed object storage
- Managed Postgres
- Managed secrets
- TLS termination
- API gateway authentication
- Network segmentation
- Private service endpoints
- Centralized logs
- Centralized metrics
- Vulnerability gates in CI