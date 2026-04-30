# Lumina Rec Model Rollback Procedure

## Purpose

This procedure defines how to roll back the inference API to a known good approved model artifact.

## Scope

This applies when:

- A new model produces bad predictions
- `/ready` fails after a model update
- Model checksum validation fails
- Load testing fails after a model update
- Inference latency increases after a model update
- A model artifact is suspected of tampering or corruption
- A deployment points to the wrong MLflow run ID

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| Dataset | MovieLens latest small |
| Model type | Matrix factorization |
| MLflow run ID | 248c55bf41994c05923a86e354158303 |
| Artifact path | approved_model |
| Model SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 |
| Test RMSE | 2.0423 |

## Rollback Triggers

Rollback should be considered if any of these occur:

- `/predict` returns repeated 500 errors
- `/ready` fails
- Checksum validation fails
- Prediction quality is worse than the previous accepted model
- Load test failure rate is above 0%
- p95 latency exceeds the accepted baseline
- The model artifact differs from the approved checksum
- The deployment references the wrong `MODEL_RUN_ID`
- Approved artifacts are missing from MLflow or MinIO

## Baseline Acceptance Criteria

| Check | Required Result |
|---|---|
| Health check | 200 OK |
| Readiness check | 200 OK |
| Prediction check | 200 OK |
| API tests | Pass |
| Load test | 0 failures |
| Checksum validation | enabled |
| Model run ID | matches approved value |
| Artifact path | approved_model |
| Model SHA256 | matches approved value |

## Environment Variables Used for Model Selection

| Variable | Purpose |
|---|---|
| MODEL_RUN_ID | MLflow run ID containing approved artifacts |
| MODEL_ARTIFACT_PATH | MLflow artifact path, currently `approved_model` |
| MODEL_SHA256 | Approved SHA256 hash for the model artifact |
| MLFLOW_TRACKING_URI | MLflow tracking server URL |
| MLFLOW_S3_ENDPOINT_URL | MinIO S3 compatible endpoint |
| AWS_ACCESS_KEY_ID | MinIO access key |
| AWS_SECRET_ACCESS_KEY | MinIO secret key |

## Rollback Steps

### 1. Identify the known good MLflow run

Open MLflow:

```text
http://localhost:5000
```

Find the previous accepted run and confirm:

- Run ID
- Model artifact path
- Model SHA256
- Test metrics
- Logged artifacts under `approved_model`

### 2. Stop inference

```powershell
docker compose stop inference
```

### 3. Update `.env`

Set the rollback values:

```env
MODEL_RUN_ID=<approved_rollback_run_id>
MODEL_ARTIFACT_PATH=approved_model
MODEL_SHA256=<approved_rollback_model_sha256>
```

Do not commit `.env`.

### 4. Confirm Docker Compose reads the rollback values

```powershell
docker compose config | Select-String "MODEL_RUN_ID|MODEL_ARTIFACT_PATH|MODEL_SHA256"
```

Expected result:

```text
MODEL_RUN_ID: <approved_rollback_run_id>
MODEL_ARTIFACT_PATH: approved_model
MODEL_SHA256: <approved_rollback_model_sha256>
```

### 5. Remove the current inference container

```powershell
docker compose rm -f inference
```

### 6. Rebuild and start inference

```powershell
docker compose up -d --build inference
```

### 7. Validate readiness

```powershell
.\scripts\lumina.ps1 ready
```

Expected result:

```text
status: ready
model_run_id: <approved_rollback_run_id>
model_artifact_path: approved_model
checksum_validation: enabled
model_sha256: <approved_rollback_model_sha256>
```

### 8. Validate prediction

```powershell
.\scripts\lumina.ps1 predict
```

Expected result:

```text
predicted_rating
user_id
movie_id
model_name
model_version
request_id
latency_ms
```

### 9. Run automated tests

```powershell
.\scripts\lumina.ps1 test
```

### 10. Run load test

```powershell
.\scripts\lumina.ps1 load-test
```

Expected result:

```text
0 failures
```

## Rollback Failure Scenarios

### MLflow run ID is wrong

Symptom:

```text
MODEL_RUN_ID is missing, invalid, or artifacts cannot be found
```

Action:

- Confirm the run exists in MLflow
- Confirm artifacts exist under `approved_model`
- Correct `MODEL_RUN_ID` in `.env`
- Restart inference

### Checksum validation fails

Symptom:

```text
Model checksum validation failed
```

Action:

- Confirm `MODEL_SHA256` matches the approved model artifact
- Recalculate the model artifact hash only from the approved artifact
- Do not bypass checksum validation unless debugging locally

### MinIO artifact access fails

Symptom:

```text
AccessDenied
NoSuchBucket
Unable to locate credentials
```

Action:

- Confirm MinIO is running
- Confirm MLflow is running
- Confirm S3 environment variables are present in Compose
- Confirm bucket and artifacts exist

## Post Rollback Review

Document:

- Reason for rollback
- Failed model run ID
- Restored model run ID
- Restored artifact path
- Restored checksum
- Validation results
- User impact
- Follow up actions

## Prevention Actions

- Require checksum approval before deployment
- Track approved artifacts in MLflow
- Compare new model metrics against baseline
- Run automated tests before serving new model
- Run load test before accepting deployment
- Keep previous known good MLflow run available
- Add MLflow Model Registry stage or alias
- Add model performance promotion gate
- Add artifact signing