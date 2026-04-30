# Local Validation Report

## Project

Lumina Rec, Local MLOps Recommendation System

## Validation Date

April 30, 2026

## Scope

This validation confirms that the local Lumina Rec MLOps stack works end to end.

The validated stack includes:

- MovieLens recommendation model training
- PyTorch matrix factorization model
- MLflow experiment tracking
- MinIO artifact storage
- Postgres backend metadata store
- Approved model artifact loading from MLflow
- FastAPI inference service
- Docker Compose orchestration
- Health and readiness checks
- Prometheus style metrics
- API key authentication for predictions and recommendations
- Configurable rate limiting
- Model checksum validation
- Automated API tests
- Locust load testing

## Services

| Service | Purpose | Local URL |
|---|---|---|
| Inference API | Serves MovieLens predictions and recommendations | http://localhost:8001 |
| MLflow | Tracks experiments and approved artifacts | http://localhost:5000 |
| MinIO | Stores MLflow artifacts | http://localhost:9001 |
| Postgres | Stores MLflow metadata | localhost:5433 |
| Redis | Future cache placeholder | localhost:6379 |
| Keycloak | Future identity provider placeholder | http://localhost:8082 |
| LocalStack | Future AWS local development placeholder | http://localhost:4566 |

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

## Commands Used

### Start Stack

```powershell
.\scripts\lumina.ps1 up
```

### Train Model

```powershell
.\scripts\lumina.ps1 train
```

Result:

```text
Training completed and logged to MLflow.
Run ID: 14eda4cf03bd4d328a3ee791ec9a002f
Model SHA256: 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd
Test RMSE: 2.0162
MLflow URL: http://localhost:5000
```

### Run Tests

```powershell
.\scripts\lumina.ps1 test
```

Expected result:

```text
tests passed
```

### Health Check

```powershell
.\scripts\lumina.ps1 health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Readiness Check

```powershell
.\scripts\lumina.ps1 ready
```

Expected response:

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

### Prediction Check

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

### Recommendation Check

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

### Metrics Check

```powershell
.\scripts\lumina.ps1 metrics
```

Expected metrics:

```text
lumina_prediction_requests_total
lumina_prediction_errors_total
lumina_prediction_latency_ms
lumina_rate_limit_errors_total
```

### Load Test

```powershell
.\scripts\lumina.ps1 load-test
```

MovieLens validation baseline:

| Metric | Result |
|---|---|
| Total requests | 446 |
| Failures | 0 |
| Failure rate | 0.00% |
| Requests per second | 7.51 |
| Health median latency | 4 ms |
| Predict median latency | 48 ms |
| Predict p95 latency | 51 ms |
| Predict max latency | 56 ms |

## Security Validation

| Control | Validation Result |
|---|---|
| API key authentication | `/predict` and `/recommend` require `x-api-key` |
| Missing API key handling | Invalid or missing key returns 401 |
| Input validation | Missing `user_id` or `movie_id` returns 422 |
| Recommendation validation | Invalid `top_n` returns 422 |
| Unknown user handling | Unknown `user_id` returns 404 |
| Unknown movie handling | Unknown `movie_id` returns 404 |
| Rate limit metric | `lumina_rate_limit_errors_total` exposed |
| Model checksum validation | `/ready` confirms checksum validation is enabled |
| Model hash visibility | `/ready` returns `model_sha256` |
| Approved artifact loading | Inference loads model artifacts from MLflow by `MODEL_RUN_ID` |
| Structured response metadata | Prediction and recommendation responses include request ID and latency |

## Conclusion

The local MLOps stack now serves a real MovieLens recommender.

The system can train a matrix factorization model, log the run to MLflow, store approved artifacts in MinIO, load approved artifacts into the inference service, verify model integrity with SHA256, serve authenticated predictions and recommendations, expose readiness and metrics, and return response metadata.

## Next Engineering Step

Recommended next steps:

- Add movie title and genre metadata to recommendation responses
- Add `/movies/{movie_id}` lookup endpoint
- Add MLflow Model Registry alias for approved models
- Add dataset checksum validation
- Add model performance promotion gate