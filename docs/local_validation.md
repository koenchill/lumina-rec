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
- API key authentication for predictions
- Configurable rate limiting
- Model checksum validation
- Automated API tests
- Locust load testing

## Services

| Service | Purpose | Local URL |
|---|---|---|
| Inference API | Serves MovieLens rating predictions | http://localhost:8001 |
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
| MLflow run ID | 248c55bf41994c05923a86e354158303 |
| Artifact path | approved_model |
| Model SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 |
| Test RMSE | 2.0423 |

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
Run ID: 248c55bf41994c05923a86e354158303
Model SHA256: c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6
Test RMSE: 2.0423
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
  "model_run_id": "248c55bf41994c05923a86e354158303",
  "model_artifact_path": "approved_model",
  "model_sha256": "c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6",
  "checksum_validation": "enabled"
}
```

### Prediction Check

```powershell
.\scripts\lumina.ps1 predict
```

Validated response:

```text
predicted_rating : 5.0
user_id          : 1
movie_id         : 1
model_name       : lumina-rec-movielens-mf
model_version    : 0.2.0
request_id       : 1df7bfd2-acaf-49a3-9443-c89160f4b9ae
latency_ms       : 9.25
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

Previous validated baseline:

| Metric | Result |
|---|---|
| Total requests | 446 |
| Failures | 0 |
| Failure rate | 0.00% |
| Requests per second | 7.54 |
| Health median latency | 4 ms |
| Predict median latency | 48 ms |
| Predict p95 latency | 51 ms |

A new load test should be rerun after the MovieLens transition to refresh the performance baseline.

## Security Validation

| Control | Validation Result |
|---|---|
| API key authentication | `/predict` requires `x-api-key` |
| Missing API key handling | Invalid or missing key returns 401 |
| Input validation | Missing `user_id` or `movie_id` returns 422 |
| Unknown user handling | Unknown `user_id` returns 404 |
| Unknown movie handling | Unknown `movie_id` returns 404 |
| Rate limit metric | `lumina_rate_limit_errors_total` exposed |
| Model checksum validation | `/ready` confirms checksum validation is enabled |
| Model hash visibility | `/ready` returns `model_sha256` |
| Approved artifact loading | Inference loads model artifacts from MLflow by `MODEL_RUN_ID` |
| Structured response metadata | Prediction includes request ID and latency |

## Conclusion

The local MLOps stack now serves a real MovieLens recommender.

The system can train a matrix factorization model, log the run to MLflow, store approved artifacts in MinIO, load approved artifacts into the inference service, verify model integrity with SHA256, serve authenticated predictions, expose readiness and metrics, and return prediction metadata.

## Next Engineering Step

Refresh validation after the MovieLens transition:

- Rerun API tests
- Rerun Locust load test
- Update the load test baseline
- Add a top N recommendation endpoint
- Add movie title metadata to prediction responses