## Current Capabilities

Lumina Rec is a local MLOps recommendation system that now supports:

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
- Pytest API tests
- Locust load testing
- Docker Compose local orchestration

## Common Commands

```powershell
.\scripts\lumina.ps1 up
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 load-test
```

## API Examples

### Predict a Movie Rating

```json
{
  "user_id": 1,
  "movie_id": 1
}
```

### Get Top N Recommendations

```json
{
  "user_id": 1,
  "top_n": 10
}
```

## Project Documentation

| Document | Purpose |
|---|---|
| [Recommendation API](docs/recommendation_api.md) | Documents `/predict` and `/recommend` |
| [Model Card](docs/model_card.md) | Documents the approved MovieLens model |
| [MLflow Artifact Strategy](docs/mlflow_artifact_strategy.md) | Explains how approved artifacts are loaded |
| [Model Promotion Record](docs/model_promotion_record.md) | Records the approved model promotion |