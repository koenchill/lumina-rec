# Lumina Rec Model Rollback Procedure

## Purpose

This procedure defines how to roll back the inference API to a known good model artifact.

## Scope

This applies when:

- A new model produces bad predictions
- `/ready` fails after a model update
- Model checksum validation fails
- Load testing fails after a model update
- Inference latency increases after a model update
- A model artifact is suspected of tampering or corruption

## Current Model

| Field | Value |
|---|---|
| Model name | lumina-rec-demo-model |
| Model version | 0.1.0 |
| Model path | ml/models/demo_model.pt |
| Checksum validation | enabled |
| Current SHA256 | 5579cbcb9e90e26c6d9f9bd3f62845c1d2aa0a8aa4eb590e5322b17d1a058903 |

## Rollback Triggers

Rollback should be considered if any of these occur:

- `/predict` returns repeated 500 errors
- `/ready` fails
- Checksum validation fails
- Prediction quality is worse than the previous accepted model
- Load test failure rate is above 0%
- p95 latency exceeds the accepted baseline
- The model artifact differs from the approved checksum

## Baseline Acceptance Criteria

| Check | Required Result |
|---|---|
| Health check | 200 OK |
| Readiness check | 200 OK |
| Prediction check | 200 OK |
| API tests | Pass |
| Load test | 0 failures |
| Checksum validation | enabled |
| Model SHA256 | matches approved value |

## Rollback Steps

### 1. Stop inference

```powershell
docker compose stop inference