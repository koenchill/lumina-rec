# Configuration Baseline

## Purpose

This file records the expected local configuration baseline.

## Runtime Variables

| Variable | Expected Local Value |
|---|---|
| MLFLOW_TRACKING_URI | http://localhost:5000 |
| MLFLOW_S3_ENDPOINT_URL | http://localhost:9000 |
| MLFLOW_EXPERIMENT_NAME | lumina-rec-recommender |
| LUMINA_API_KEY | local-dev-api-key |
| LUMINA_RATE_LIMIT | 300/minute |
| MODEL_ARTIFACT_PATH | approved_model |
| REGISTERED_MODEL_NAME | lumina-rec-movielens-mf |
| MODEL_ALIAS | approved |

## Approved Model Values

| Variable | Value |
|---|---|
| MODEL_RUN_ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| MODEL_SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |

## Docker Ports

| Service | Host Port |
|---|---|
| inference | 8001 |
| mlflow | 5000 |
| minio api | 9000 |
| minio console | 9001 |
| postgres | 5433 |
| redis | 6379 |
| keycloak | 8082 |
| localstack | 4566 |