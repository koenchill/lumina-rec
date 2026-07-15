# Production Deployment Plan

## Purpose

This document outlines the future production deployment path for Lumina Rec.

## Current State

Lumina Rec runs locally with Docker Compose for MLflow/MinIO/Postgres, optional
Compose inference, plus Kubernetes inference managed by local Terraform.

Current local services:

| Service | Purpose |
|---|---|
| inference | FastAPI inference API (Compose `:8001` and/or Kubernetes `:8002`) |
| mlflow | MLflow tracking server |
| minio | Artifact storage |
| postgres | MLflow metadata store |

## Target Production Pattern

| Component | Production Target |
|---|---|
| Inference API | Container service |
| Model artifacts | Managed object storage |
| Metadata store | Managed Postgres |
| Secrets | Managed secret store |
| Authentication | API gateway or JWT provider |
| Monitoring | Prometheus and Grafana |
| Logging | Centralized log platform |
| CI CD | GitHub Actions or enterprise pipeline |

## Deployment Requirements

- TLS enabled
- Private network for backend services
- Secrets stored outside code
- API authentication enforced
- Metrics restricted to internal monitoring
- Container images scanned
- Model artifacts verified by checksum
- Rollback path documented

## Future Infrastructure Tasks

1. Add cloud Terraform environments (beyond local Kubernetes provider).
2. Add container registry workflow.
3. Add environment specific configuration.
4. Add production secret manager pattern.
5. Add API gateway design.
6. Add monitoring dashboard.
7. Add rollback automation.