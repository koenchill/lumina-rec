# Environment Variables

## Purpose

This file documents the environment variables used by Lumina Rec.

## Local `.env`

Do not commit `.env`.

## MLflow and Artifact Storage

| Variable | Example | Purpose |
|---|---|---|
| MLFLOW_TRACKING_URI | http://localhost:5000 | Local MLflow tracking server |
| MLFLOW_S3_ENDPOINT_URL | http://localhost:9000 | Local MinIO S3 endpoint |
| AWS_ACCESS_KEY_ID | minio | MinIO access key |
| AWS_SECRET_ACCESS_KEY | minio123 | MinIO secret key |
| MLFLOW_EXPERIMENT_NAME | lumina-rec-recommender | MLflow experiment name |

## Inference Security

| Variable | Example | Purpose |
|---|---|---|
| LUMINA_API_KEY | local-dev-api-key | API key required for `/predict` and `/recommend` |
| LUMINA_RATE_LIMIT | 300/minute | Local rate limit for protected endpoints |

## Approved Model Selection

| Variable | Example | Purpose |
|---|---|---|
| MODEL_RUN_ID | 248c55bf41994c05923a86e354158303 | MLflow run ID for approved artifacts |
| MODEL_ARTIFACT_PATH | approved_model | Artifact folder in the MLflow run |
| MODEL_SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 | Approved model checksum |
| APPROVED_MODEL_DIR | ml/models/approved | Local artifact download cache |

## Docker Compose Notes

Inside Docker Compose, `MLFLOW_TRACKING_URI` must use the service name:

```text
http://mlflow:5000