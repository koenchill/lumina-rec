# Lumina Rec

## Purpose

Lumina Rec is a local MLOps recommendation system.

It demonstrates how to train a recommendation model, track experiments, store approved artifacts, load the approved model into an inference API, validate model integrity, and serve predictions through a local Docker Compose stack.

## Current Capabilities

Lumina Rec currently supports:

- MovieLens matrix factorization model training
- MLflow experiment tracking
- MinIO model artifact storage
- Postgres MLflow metadata storage
- Approved model loading by MLflow run ID
- SHA256 model checksum validation
- FastAPI inference service
- API key authentication
- Rate limiting
- Prometheus metrics
- Structured JSON logs
- Rating prediction with `/predict`
- Top N recommendations with `/recommend`
- Movie title and genre metadata in recommendation responses
- Movie metadata lookup with `/movies/{movie_id}`
- Pytest API tests
- Locust load testing
- Docker Compose local orchestration

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

## Local Services

| Service | Purpose | Local URL |
|---|---|---|
| Inference API | Serves predictions, recommendations, and movie metadata | http://localhost:8001 |
| MLflow | Tracks experiments and approved artifacts | http://localhost:5000 |
| MinIO | Stores MLflow artifacts | http://localhost:9001 |
| Postgres | Stores MLflow metadata | localhost:5433 |
| Redis | Future cache placeholder | localhost:6379 |
| Keycloak | Future identity provider placeholder | http://localhost:8082 |
| LocalStack | Future AWS local development placeholder | http://localhost:4566 |

## Common Commands

```powershell
.\scripts\lumina.ps1 up
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 load-test
```

## API Examples

### Predict a Movie Rating

Request:

```json
{
  "user_id": 1,
  "movie_id": 1
}
```

Response fields:

```text
predicted_rating
user_id
movie_id
model_name
model_version
request_id
latency_ms
```

### Get Top N Recommendations

Request:

```json
{
  "user_id": 1,
  "top_n": 10
}
```

Response example:

```json
{
  "user_id": 1,
  "recommendations": [
    {
      "movie_id": 2,
      "title": "Jumanji (1995)",
      "genres": "Adventure|Children|Fantasy",
      "predicted_rating": 5.0
    }
  ],
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0",
  "request_id": "example-request-id",
  "latency_ms": 3.83
}
```

### Look Up Movie Metadata

Request:

```http
GET /movies/1
```

Response:

```json
{
  "movie_id": 1,
  "title": "Toy Story (1995)",
  "genres": "Adventure|Animation|Children|Comedy|Fantasy"
}
```

## Local Runtime Values

Set these in `.env`.

Do not commit `.env`.

```env
AWS_ACCESS_KEY_ID=minio
AWS_SECRET_ACCESS_KEY=minio123
MLFLOW_S3_ENDPOINT_URL=http://localhost:9000
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=lumina-rec-recommender

LUMINA_API_KEY=local-dev-api-key
LUMINA_RATE_LIMIT=300/minute

MODEL_RUN_ID=14eda4cf03bd4d328a3ee791ec9a002f
MODEL_SHA256=205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd
MODEL_ARTIFACT_PATH=approved_model
```

## Quick Validation

Run:

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 test
```

Expected result:

- `/ready` returns approved model metadata and checksum status
- `/predict` returns a rating prediction
- `/recommend` returns recommendations with movie title and genre metadata
- `/movies/{movie_id}` returns title and genre metadata
- API tests pass

## Project Documentation

Start at [docs/README.md](docs/README.md). Key entry points:

| Document | Purpose |
|---|---|
| [Architecture](docs/architecture/architecture.md) | Local MLOps architecture and service flow |
| [API Contract](docs/api/api_contract.md) | Endpoints, headers, request/response shapes |
| [Repository Structure](docs/project/repository_structure.md) | Folders and ownership after reorg |
| [Model Card](docs/mlops/model_card.md) | Approved MovieLens model |
| [Runbook Quickstart](docs/operations/runbook_quickstart.md) | Fastest local validation path |
| [Developer Setup](docs/operations/developer_setup.md) | Local setup steps |
| [Security Controls](docs/security/security_controls.md) | Implemented controls |
| [Threat Model](docs/security/threat_model.md) | Threats and mitigations |
| [Project Status](docs/project/project_status.md) | Current state and next steps |
| [Next Steps / Plans](docs/plans/) | Future engineering work |

## Files Not To Commit

```text
.env
.venv/
ml/models/approved/
ml/models/*.pt
ml/models/*.json
ml/models/*.csv
tests/load/load_test_report.html
__pycache__/
*.pyc
.pytest_cache/
```

## Next Build Task

Default approved model selection to MLflow Model Registry alias.