# Lumina Rec Architecture

## Purpose

Lumina Rec is a local MLOps recommendation system that demonstrates model training, experiment tracking, artifact storage, containerized inference, observability, and security controls.

The current model is a MovieLens matrix factorization recommender trained on the MovieLens latest small dataset.

## Architecture Diagram

```mermaid
flowchart LR
    Developer[Developer]
    Train[PyTorch Training Script]
    Dataset[(MovieLens Dataset)]
    MLflow[MLflow Tracking Server]
    Postgres[(Postgres Metadata Store)]
    MinIO[(MinIO Artifact Store)]
    Client[Client]
    API[FastAPI Inference API]
    Approved[Approved MLflow Model Artifact]
    Model[MovieLens Matrix Factorization Model]
    Metrics[Prometheus Metrics]
    Logs[Structured JSON Logs]

    Developer --> Train
    Dataset --> Train
    Train --> MLflow
    MLflow --> Postgres
    MLflow --> MinIO
    MinIO --> Approved

    Client -->|POST /predict with x-api-key| API
    API -->|downloads approved artifact by MODEL_RUN_ID| MLflow
    API -->|verifies SHA256| Approved
    Approved --> Model
    Model --> API
    API --> Client
    API --> Metrics
    API --> Logs
```

## Training Flow

The training workflow:

1. Downloads the MovieLens latest small dataset.
2. Trains a PyTorch matrix factorization recommender.
3. Logs parameters and metrics to MLflow.
4. Saves the approved model artifact.
5. Logs model metadata, mappings, and movie metadata to MLflow.
6. Records the model SHA256 checksum.

Current approved run:

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 248c55bf41994c05923a86e354158303 |
| Artifact path | approved_model |
| Model SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 |
| Dataset | MovieLens latest small |

## Inference Flow

The inference service:

1. Reads `MODEL_RUN_ID`.
2. Connects to MLflow.
3. Downloads artifacts from the `approved_model` path.
4. Loads `recommender_model.pt`.
5. Loads `model_metadata.json`.
6. Loads `movielens_mappings.json`.
7. Verifies the model SHA256 checksum.
8. Serves predictions through `/predict`.

## Local Services

| Service | Role | URL |
|---|---|---|
| FastAPI Inference | Serves MovieLens rating predictions | http://localhost:8001 |
| MLflow | Tracks experiments and approved model artifacts | http://localhost:5000 |
| MinIO | Stores MLflow artifacts | http://localhost:9001 |
| Postgres | Stores MLflow metadata | localhost:5433 |
| Redis | Future cache and queue support | localhost:6379 |
| Keycloak | Future identity provider | http://localhost:8082 |
| LocalStack | Future AWS local testing | http://localhost:4566 |

## Inference API

The inference API exposes:

| Endpoint | Purpose | Protection |
|---|---|---|
| GET /health | Confirms service is running | Open locally |
| GET /ready | Confirms approved MLflow model artifact is loaded | Open locally |
| GET /metrics | Exposes metrics | Open locally |
| POST /predict | Predicts a MovieLens rating | Requires API key |

## Prediction Request

```json
{
  "user_id": 1,
  "movie_id": 1
}
```

## Prediction Response

```json
{
  "predicted_rating": 5.0,
  "user_id": 1,
  "movie_id": 1,
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0",
  "request_id": "example-request-id",
  "latency_ms": 9.25
}
```

## Security Controls

Current controls include:

- API key authentication for `/predict`
- Input validation with Pydantic
- Unknown user and movie rejection
- Configurable rate limiting
- Model checksum validation
- Approved model loading through MLflow
- Structured JSON logs
- Prometheus metrics
- Secret scanning in CI
- Container vulnerability scanning in CI
- Dockerized inference runtime
- `.env` excluded from Git

## Observability

The system exposes:

- Request count
- Prediction error count
- Prediction latency
- Rate limit error count
- Structured logs with request ID
- Model checksum status from `/ready`
- Model run ID from `/ready`
- Artifact path from `/ready`

## Model Integrity

The inference service calculates SHA256 for the approved model artifact.

If `MODEL_SHA256` is set and does not match the downloaded MLflow artifact, the service fails startup.

Current approved checksum:

```text
c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6
```

## Local Validation

The current stack has validated:

- MovieLens training completed
- MLflow run logged
- Approved artifacts stored in MinIO
- Inference service downloaded approved artifacts
- `/health` passed
- `/ready` passed
- `/predict` passed with `user_id` and `movie_id`
- `/metrics` passed
- API tests passed
- Load test passed before the MovieLens transition

## Future Architecture Improvements

- Improve model performance beyond baseline RMSE
- Add top N recommendation endpoint
- Add movie metadata to prediction response
- Add Feast feature store workflow
- Add JWT based authentication
- Restrict metrics to internal monitoring
- Add Grafana dashboard
- Add production cloud deployment path