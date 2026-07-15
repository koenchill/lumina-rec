# Runbook Quickstart

## Purpose

This file gives the shortest path to run and validate Lumina Rec locally.

## Prerequisites

1. Docker Desktop is running.
2. `.env` exists (copy from `.env.example` if needed).
3. `MODEL_RUN_ID` and `MODEL_SHA256` in `.env` point at a run that exists in **this**
   local MLflow/MinIO stack.

## Start Core Stack

```powershell
.\scripts\lumina.ps1 up
```

This starts postgres, minio, minio-init (creates `mlflow-artifacts`), mlflow, and
inference. Optional placeholders (redis, keycloak, localstack) stay off unless you use:

```powershell
docker compose --profile extras up -d
```

## Confirm Services

```powershell
docker compose ps
```

Core services should be healthy (minio-init exits 0 after creating the bucket).

## If Inference Is Unhealthy

Missing MLflow run (common after a fresh compose volume):

```text
RESOURCE_DOES_NOT_EXIST: Run with id=... not found
```

Train and re-pin:

```powershell
$env:PYTHONPATH = "src;."
.\.venv\Scripts\python.exe .\ml\training\train.py
```

Update `.env` from `reports/latest_training_run.json` (`model_run_id`, `model_sha256`),
then:

```powershell
docker compose up -d --force-recreate inference
.\scripts\lumina.ps1 ready
```

Also clear accidental shell overrides:

```powershell
Remove-Item Env:MODEL_RUN_ID -ErrorAction SilentlyContinue
Remove-Item Env:MODEL_SHA256 -ErrorAction SilentlyContinue
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

## Expected Movie Lookup Response Fields

```text
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

Then restart inference after fixing `.env`:

```powershell
docker compose up -d --force-recreate inference
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
