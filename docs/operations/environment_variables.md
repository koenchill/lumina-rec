# Environment Variables

## Purpose

This file documents the environment variables used by Lumina Rec.

## Local `.env`

Do not commit `.env`.

The local `.env` file controls MLflow access, MinIO access, API authentication, rate limiting, and approved model selection.

## MLflow and Artifact Storage

| Variable | Example | Purpose |
|---|---|---|
| MLFLOW_TRACKING_URI | http://localhost:5000 | Local MLflow tracking server for host training |
| MLFLOW_S3_ENDPOINT_URL | http://localhost:9000 | Local MinIO S3 endpoint for host training |
| AWS_ACCESS_KEY_ID | minio | MinIO access key |
| AWS_SECRET_ACCESS_KEY | minio123 | MinIO secret key |
| MLFLOW_EXPERIMENT_NAME | lumina-rec-recommender | MLflow experiment name |

## Docker Compose MLflow Values

Inside Docker Compose, the inference service uses service names, not localhost.

| Variable | Example | Purpose |
|---|---|---|
| MLFLOW_TRACKING_URI | http://mlflow:5000 | MLflow URL from inside the Docker network |
| MLFLOW_S3_ENDPOINT_URL | http://minio:9000 | MinIO URL from inside the Docker network |

## Inference Security

| Variable | Example | Purpose |
|---|---|---|
| LUMINA_API_KEY | local-dev-api-key | API key required for `/predict` and `/recommend` |
| LUMINA_RATE_LIMIT | 300/minute | Local rate limit for protected endpoints |

## Approved Model Selection

Compose requires `MODEL_RUN_ID` and `MODEL_SHA256`. They must exist in the **current**
local MLflow/MinIO data. After a fresh stack, train and copy values from
`reports/latest_training_run.json`.

| Variable | Example / Source | Purpose |
|---|---|---|
| MODEL_RUN_ID | from `reports/latest_training_run.json` | MLflow run ID for approved artifacts |
| MODEL_ARTIFACT_PATH | approved_model | Artifact folder in the MLflow run |
| MODEL_SHA256 | from `reports/latest_training_run.json` | Approved model checksum |
| APPROVED_MODEL_DIR | ml/models/approved | Local artifact download cache |

See `.env.example` for the full local template.

## Runtime Validation

Confirm Docker Compose sees the model pin values from `.env`:

```powershell
docker compose config | Select-String "MODEL_RUN_ID|MODEL_SHA256|MODEL_ARTIFACT_PATH"
```

Shell environment variables override `.env`. Clear accidental overrides before compose:

```powershell
Remove-Item Env:MODEL_RUN_ID -ErrorAction SilentlyContinue
Remove-Item Env:MODEL_SHA256 -ErrorAction SilentlyContinue
```

## Safety Rules

- Do not commit `.env`.
- Rotate credentials if `.env` is exposed.
- Update `MODEL_SHA256` when approving a new model.
- Update `MODEL_RUN_ID` when promoting a new MLflow run.
- Keep the previous approved run ID and checksum before promotion.
- Do not promote a new model without validation.