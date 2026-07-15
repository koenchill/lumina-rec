# Lumina Rec Next Steps

## Purpose

This file tracks the next engineering tasks for the Lumina Rec local MLOps stack.

## Current Stable Baseline

The current stable stack includes:

- MovieLens matrix factorization recommender
- MLflow experiment tracking
- MinIO artifact storage
- Postgres metadata storage
- FastAPI inference service
- Approved model loading by MLflow run ID
- SHA256 model checksum validation
- API key authentication
- Configurable rate limiting
- Prometheus metrics
- Structured logs
- `/predict` endpoint for rating prediction
- `/recommend` endpoint for top N recommendations
- Pytest API tests
- Locust load testing
- GitHub Actions CI
- Secret scanning
- Container vulnerability scanning

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| Dataset | MovieLens latest small |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Immediate Next Tasks

1. Add movie title and genre metadata to `/recommend` responses.
2. Add `/movies/{movie_id}` lookup endpoint.
3. Update API tests for movie metadata.
4. Update Locust load test to include `/recommend`.
5. Add MLflow Model Registry alias or stage for approved models.

## Model Governance Tasks

| Task | Priority | Purpose |
|---|---|---|
| MLflow Model Registry alias | High | Avoid hard coding approved run ID |
| Dataset checksum validation | High | Validate training data integrity |
| Model performance gate | High | Prevent promotion of weaker models |
| Artifact manifest validation | Medium | Confirm model, metadata, and mappings belong together |
| Signed artifact verification | Medium | Improve model supply chain integrity |

## API Improvement Tasks

| Task | Priority | Purpose |
|---|---|---|
| Add movie metadata to recommendations | High | Make recommendations readable |
| Add movie lookup endpoint | High | Support movie title and genre lookup |
| Add top genre filter | Medium | Improve recommendation flexibility |
| Add batch prediction endpoint | Medium | Predict ratings for many movies |
| Add recommendation explanation field | Low | Improve user trust |

## Security Improvement Tasks

| Task | Priority | Purpose |
|---|---|---|
| Replace API key with JWT | High | Improve authentication |
| Restrict `/metrics` | High | Prevent metric exposure |
| Add gateway rate limiting | Medium | Improve abuse protection |
| Enforce Trivy critical failure | Medium | Improve vulnerability gate |
| Add secret manager pattern | Medium | Replace local `.env` pattern |

## Observability Tasks

| Task | Priority | Purpose |
|---|---|---|
| Add Grafana dashboard | Medium | Visualize latency and errors |
| Add recommendation latency metric | Medium | Track `/recommend` performance |
| Add model run ID metric | Medium | Expose current serving model |
| Add structured error dashboard | Low | Improve incident review |

## Deployment Tasks

| Task | Priority | Purpose |
|---|---|---|
| Add production deployment guide | Medium | Define cloud deployment path |
| Add Terraform skeleton | Medium | Prepare infrastructure as code |
| Add container registry workflow | Medium | Prepare image publishing |
| Add environment specific configs | Low | Separate dev and prod values |