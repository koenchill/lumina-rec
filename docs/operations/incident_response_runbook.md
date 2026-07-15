# Lumina Rec Inference API Incident Response Runbook

## Purpose

This runbook defines how to detect, triage, contain, and recover from issues affecting the Lumina Rec inference API.

## Scope

This runbook covers:

- Inference API outage
- Failed health or readiness checks
- Prediction errors
- High latency
- Rate limit spikes
- Authentication failures
- Model checksum validation failure
- Container startup failure
- MLflow, MinIO, or Postgres dependency issues

## Key Services

| Service | Purpose | Local URL |
|---|---|---|
| Inference API | Serves predictions | http://localhost:8001 |
| MLflow | Tracks experiments and artifacts | http://localhost:5000 |
| MinIO | Stores model artifacts | http://localhost:9001 |
| Postgres | Stores MLflow metadata | localhost:5433 |
| Redis | Cache placeholder | localhost:6379 |

## Quick Status Checks

### Check running containers

```powershell
docker compose ps