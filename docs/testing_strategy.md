# Testing Strategy

## Purpose

This document explains how Lumina Rec validates the local MLOps stack.

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Test Types

| Test Type | Tool | Purpose |
|---|---|---|
| API tests | Pytest | Validate endpoint behavior |
| Load tests | Locust | Validate repeated API requests |
| Health checks | PowerShell runner | Confirm service availability |
| Readiness checks | PowerShell runner | Confirm approved model loaded |
| CI checks | GitHub Actions | Validate code, container, and security checks |

## API Test Coverage

The test suite validates:

- Health endpoint
- Readiness endpoint
- Prediction endpoint
- Recommendation endpoint
- Missing API key rejection
- Invalid API key rejection
- Missing required fields
- Invalid `top_n` handling
- Unknown user handling
- Unknown movie handling
- Metrics endpoint

## Endpoint Validation Matrix

| Endpoint | Test Focus | Expected Result |
|---|---|---|
| GET /health | Service availability | 200 OK |
| GET /ready | Approved model metadata | 200 OK with model run ID and checksum |
| POST /predict | Rating prediction | 200 OK with `predicted_rating` |
| POST /recommend | Top N recommendations | 200 OK with recommendation list |
| GET /metrics | Metrics exposure | 200 OK with Prometheus metrics |

## Load Test Coverage

The Locust test validates:

- GET /health
- POST /predict
- Required response fields
- Zero failure baseline

Future load test coverage should include:

- POST /recommend
- Larger `top_n` values
- Unknown user requests
- Rate limit behavior

## Commands

```powershell
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 load-test
```

## Acceptance Criteria

| Check | Required Result |
|---|---|
| API tests | Pass |
| Load test failures | 0 |
| Health endpoint | 200 |
| Ready endpoint | 200 |
| Predict endpoint | 200 |
| Recommend endpoint | 200 |
| Metrics endpoint | 200 |
| Checksum validation | enabled |
| Model run ID | matches approved run |