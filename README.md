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

## Project Documentation

| Document | Purpose |
|---|---|
| [Architecture](docs/architecture.md) | Explains the local MLOps architecture and service flow |
| [API Contract](docs/api_contract.md) | Defines endpoints, request headers, request body, and responses |
| [Recommendation API](docs/recommendation_api.md) | Documents `/predict` and `/recommend` |
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