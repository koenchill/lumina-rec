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

| Document | Purpose |
|---|---|
| [Architecture](docs/architecture.md) | Explains the local MLOps architecture and service flow |
| [API Contract](docs/api_contract.md) | Defines endpoints, request headers, request body, and responses |
| [Recommendation API](docs/recommendation_api.md) | Documents `/predict`, `/recommend`, and movie lookup |
| [Model Card](docs/model_card.md) | Documents the approved MovieLens model |
| [Model Promotion Record](docs/model_promotion_record.md) | Records the approved model promotion |
| [MLflow Artifact Strategy](docs/mlflow_artifact_strategy.md) | Explains how approved artifacts are loaded |
| [Environment Variables](docs/environment_variables.md) | Documents local runtime configuration |
| [Operational Commands](docs/operational_commands.md) | Lists common local commands |
| [Runbook Quickstart](docs/runbook_quickstart.md) | Gives the fastest local validation path |
| [Repository Structure](docs/repository_structure.md) | Explains project folders and files |
| [Testing Strategy](docs/testing_strategy.md) | Explains API and load test coverage |
| [Security Controls](docs/security_controls.md) | Maps implemented controls to risk reduction |
| [Threat Model](docs/threat_model.md) | Identifies threats, gaps, and planned controls |
| [Local Validation Report](docs/local_validation.md) | Records proof that the local stack works end to end |
| [Incident Response Runbook](docs/incident_response_runbook.md) | Provides troubleshooting and recovery steps |
| [Model Rollback Procedure](docs/model_rollback_procedure.md) | Defines how to restore a known good model |
| [Deployment Notes](docs/deployment_notes.md) | Captures Docker and local deployment decisions |
| [Project Status](docs/project_status.md) | Summarizes current state and next steps |
| [Docker Cleanup Notes](docs/docker_cleanup.md) | Shows safe Docker cleanup commands |
| [Next Steps](docs/next_steps.md) | Tracks future engineering work |
| [CI CD Strategy](docs/ci_cd_strategy.md) | Defines CI validation goals |
| [Observability Plan](docs/observability_plan.md) | Defines metrics, logs, and dashboards |
| [Model Registry Plan](docs/model_registry_plan.md) | Plans MLflow registry based promotion |
| [Dataset Validation Plan](docs/dataset_validation_plan.md) | Defines dataset quality checks |
| [Production Deployment Plan](docs/production_deployment_plan.md) | Outlines production deployment target |
| [API Security Plan](docs/api_security_plan.md) | Defines API security improvements |
| [Monitoring Metrics](docs/monitoring_metrics.md) | Defines current and target metrics |
| [Recommendation Quality Plan](docs/recommendation_quality_plan.md) | Defines ranking quality metrics |
| [Release Notes](docs/release_notes.md) | Summarizes current release changes |
| [Handoff Summary](docs/handoff_summary.md) | Summarizes project state for handoff |
| [Movie Metadata Enrichment Plan](docs/movie_metadata_enrichment_plan.md) | Plans title and genre enrichment |
| [Feature Store Plan](docs/feature_store_plan.md) | Plans Feast based feature management |
| [Model Performance Gate](docs/model_performance_gate.md) | Defines promotion performance checks |
| [Artifact Manifest Plan](docs/artifact_manifest_plan.md) | Plans artifact integrity validation |
| [Secrets Management Plan](docs/secrets_management_plan.md) | Defines future secrets management |
| [Rate Limiting Plan](docs/rate_limiting_plan.md) | Defines rate limiting controls |
| [Logging Standard](docs/logging_standard.md) | Defines structured logging rules |
| [Error Handling Standard](docs/error_handling_standard.md) | Defines safe API error behavior |
| [Developer Setup](docs/developer_setup.md) | Shows local setup steps |
| [Maintenance Plan](docs/maintenance_plan.md) | Defines routine maintenance tasks |
| [Final Checkpoint](docs/final_checkpoint.md) | Records the current working project checkpoint |

## Files Not To Commit

```text
.env
.venv/
ml/models/approved/
ml/models/*.pt
tests/load/load_test_report.html
__pycache__/
*.pyc
.pytest_cache/
```

## Next Build Task

Add MLflow Model Registry alias for approved model selection.