# Operational Commands

## Purpose

This file lists common commands for operating Lumina Rec locally.

## Start Stack

```powershell
.\scripts\lumina.ps1 up
```

## Stop Stack

```powershell
.\scripts\lumina.ps1 down
```

## Show Services

```powershell
.\scripts\lumina.ps1 ps
```

## Show Logs

```powershell
.\scripts\lumina.ps1 logs
```

## Train Model

```powershell
.\scripts\lumina.ps1 train
```

## Run Tests

```powershell
.\scripts\lumina.ps1 test
```

## Check Health

```powershell
.\scripts\lumina.ps1 health
```

## Check Readiness

```powershell
.\scripts\lumina.ps1 ready
```

## Predict Rating

```powershell
.\scripts\lumina.ps1 predict
```

Expected response fields:

```text
predicted_rating
user_id
movie_id
model_name
model_version
request_id
latency_ms
```

## Get Top N Recommendations

```powershell
.\scripts\lumina.ps1 recommend
```

Expected response fields:

```text
user_id
recommendations
model_name
model_version
request_id
latency_ms
```

## Get Movie Metadata

```powershell
.\scripts\lumina.ps1 movie
```

Expected response fields:

```text
movie_id
title
genres
```

## Get Movie Metadata

```powershell
.\scripts\lumina.ps1 movie
```

Expected response fields:

```text
movie_id
title
genres
```

## Metrics

```powershell
.\scripts\lumina.ps1 metrics
```

## Load Test

```powershell
.\scripts\lumina.ps1 load-test
```

## Docker Commands

```powershell
docker compose ps
docker compose logs inference --tail=100
docker compose up -d --build inference
docker compose down
```

## MLflow Commands

```powershell
Invoke-WebRequest -Uri http://localhost:5000 -UseBasicParsing
```

## MinIO Bucket Check

```powershell
docker compose exec minio mc ls local
```

Expected bucket:

```text
mlflow-artifacts
```

## Model Promotion Check

```powershell
docker compose config | Select-String "MODEL_RUN_ID|MODEL_SHA256|MODEL_ARTIFACT_PATH"
```

Expected approved values:

```text
MODEL_RUN_ID: 14eda4cf03bd4d328a3ee791ec9a002f
MODEL_SHA256: 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd
MODEL_ARTIFACT_PATH: approved_model
```

## Git Commands

```powershell
git status
git add .
git commit -m "message"
git push
```

## Files Not To Commit

```text
.env
.venv/
ml/models/approved/
tests/load/load_test_report.html
__pycache__/
*.pyc
```