# Roadmap

## Purpose

This roadmap defines the next phases for Lumina Rec.

## Phase 1, Local MLOps Baseline

Status: Complete

Delivered:

- Docker Compose stack
- MLflow tracking
- MinIO artifact storage
- Postgres metadata store
- FastAPI inference
- MovieLens model training
- Approved model artifact loading
- SHA256 validation
- `/predict`
- `/recommend`
- API tests
- Load testing
- Documentation

## Phase 2, Recommendation Usability

Status: In progress

Planned:

- Add movie title and genre metadata to recommendation responses
- Add `/movies/{movie_id}` lookup endpoint
- Add recommendation load test coverage
- Update API docs and tests

## Phase 3, Model Governance

Status: Planned

Planned:

- MLflow Model Registry alias
- Model promotion workflow
- Dataset checksum validation
- Artifact manifest validation
- Model performance gate

## Phase 4, Production Readiness

Status: Planned

Planned:

- API gateway authentication
- Managed secrets
- TLS
- Restricted metrics
- Centralized logs
- Grafana dashboards
- Production deployment guide
- Terraform skeleton