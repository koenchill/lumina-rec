# Interview Talking Points

## Purpose

This document helps explain Lumina Rec in interviews or portfolio reviews.

## Short Pitch

Lumina Rec is a local MLOps recommendation system that moves a MovieLens model from training to approved artifact storage, then serves it through an authenticated FastAPI inference API.

## Technical Talking Points

| Topic | Talking Point |
|---|---|
| MLOps | MLflow tracks model runs, metrics, and artifacts |
| Artifact storage | MinIO stores approved model artifacts locally |
| Model serving | FastAPI serves prediction and recommendation endpoints |
| Model integrity | SHA256 validates the approved model before serving |
| Security | API key protects prediction and recommendation endpoints |
| Observability | Prometheus metrics and structured logs support operations |
| Testing | Pytest validates API behavior |
| Load testing | Locust validates local performance |
| Governance | Promotion, rollback, threat model, and runbooks are documented |

## STAR Example

Situation: A model needed a safe local serving path.

Task: Build an end to end MLOps workflow from training to inference.

Action: Added MLflow tracking, MinIO artifact storage, checksum validation, FastAPI endpoints, API tests, load tests, and documentation.

Result: The system serves MovieLens predictions and recommendations from an approved model artifact with validation and rollback procedures.