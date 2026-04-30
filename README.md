# Lumina Rec

Lumina Rec is a local MLOps recommendation system that demonstrates model training, experiment tracking, artifact storage, and containerized inference.

## Current Architecture

The local stack includes:

| Component | Purpose | Local URL |
|---|---|---|
| FastAPI Inference | Serves model predictions | http://localhost:8001 |
| MLflow | Tracks experiments and model artifacts | http://localhost:5000 |
| MinIO | Stores MLflow artifacts | http://localhost:9001 |
| Postgres | MLflow backend database | localhost:5433 |
| Redis | Cache and future queue support | localhost:6379 |
| Keycloak | Identity provider placeholder | http://localhost:8082 |
| LocalStack | AWS local development placeholder | http://localhost:4566 |

## Start the Stack

```powershell
docker compose up -d --build

## Current Capabilities

- PyTorch baseline model training
- MLflow experiment tracking
- MinIO artifact storage
- FastAPI inference API
- API key authentication on `/predict`
- Configurable rate limiting
- Model checksum validation
- Prometheus metrics at `/metrics`
- Structured JSON logs
- Docker Compose local stack
- CPU only PyTorch inference image
- Pytest API tests
- Locust load testing
- GitHub Actions CI with tests, Docker build, health checks, secret scan, and container scan

## Common Commands

```powershell
.\scripts\lumina.ps1 up
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 load-test