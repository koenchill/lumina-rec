# Local Validation Report

## Project

Lumina Rec, Local MLOps Recommendation System

## Validation Date

April 29, 2026

## Scope

This validation confirms that the local MLOps stack works end to end.

The validated stack includes:

- PyTorch model training
- MLflow experiment tracking
- MinIO artifact storage
- Postgres backend metadata store
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
| Inference API | Serves predictions | http://localhost:8001 |
| MLflow | Tracks experiments and artifacts | http://localhost:5000 |
| MinIO | Stores MLflow artifacts | http://localhost:9001 |
| Postgres | Stores MLflow metadata | localhost:5433 |
| Redis | Cache placeholder | localhost:6379 |
| Keycloak | Identity provider placeholder | http://localhost:8082 |
| LocalStack | AWS local development placeholder | http://localhost:4566 |

## Commands Used

### Start Stack

```powershell
.\scripts\lumina.ps1 up