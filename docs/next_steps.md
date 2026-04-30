# Lumina Rec Next Steps

## Purpose

This file tracks the next engineering tasks for the Lumina Rec local MLOps stack.

## Current Stable Baseline

The current stable stack includes:

- FastAPI inference service
- API key authentication
- Configurable rate limiting
- Model checksum validation
- Prometheus metrics
- Structured logs
- MLflow tracking
- MinIO artifact storage
- Postgres metadata store
- Pytest API tests
- Locust load testing
- GitHub Actions CI
- Secret scanning
- Container vulnerability scanning

## Deferred Task

### Pin inference container dependencies

Status: Deferred

Reason:

Docker Desktop had engine availability and package download timing issues during the build process.

Goal:

Create a pinned `services/inference/requirements.txt` and update the inference Dockerfile to use pinned package versions.

Target dependencies:

```text
fastapi==0.136.1
uvicorn==0.46.0
pydantic==2.13.3
numpy==2.4.4
prometheus-client==0.25.0
python-dotenv==1.2.2
slowapi==0.1.9