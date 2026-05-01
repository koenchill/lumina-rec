# Runbook Quickstart

## Purpose

This file gives the shortest path to run and validate Lumina Rec locally.

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Start Required Services

```powershell
docker compose up -d postgres minio mlflow
```

## Confirm MLflow

```powershell
Invoke-WebRequest -Uri http://localhost:5000 -UseBasicParsing
```

Expected result:

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

## Confirm Model Runtime Values

```powershell
docker compose config | Select-String "MODEL_RUN_ID|MODEL_SHA256|MODEL_ARTIFACT_PATH"
```

Expected values:

```text
MODEL_RUN_ID: 14eda4cf03bd4d328a3ee791ec9a002f
MODEL_SHA256: 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd
MODEL_ARTIFACT_PATH: approved_model
```

## Start Inference

```powershell
docker compose up -d --build inference
```

## Validate API

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
```

## Expected Predict Response Fields

```text
predicted_rating
user_id
movie_id
model_name
model_version
request_id
latency_ms
```

## Expected Recommend Response Fields

```text
user_id
recommendations
model_name
model_version
request_id
latency_ms
movie_id
title
genres
```

## Run Tests

```powershell
.\scripts\lumina.ps1 test
```

## Run Load Test

```powershell
.\scripts\lumina.ps1 load-test
```

## Common Failure

If inference does not become ready, check logs:

```powershell
docker compose logs inference --tail=120
```

If logs show an old or missing run ID, update `.env`:

```env
MODEL_RUN_ID=14eda4cf03bd4d328a3ee791ec9a002f
MODEL_SHA256=205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd
MODEL_ARTIFACT_PATH=approved_model
```

Then restart inference:

```powershell
docker compose stop inference
docker compose rm -f inference
docker compose up -d --build inference
```

## Do Not Commit

```text
.env
.venv/
ml/models/approved/
tests/load/load_test_report.html
__pycache__/
*.pyc
```