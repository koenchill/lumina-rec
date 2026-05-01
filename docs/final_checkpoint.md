# Final Checkpoint

## Project

Lumina Rec

## Status

The local MLOps recommendation system is working, documented, and now returns movie metadata in recommendation responses.

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Working Endpoints

| Endpoint | Status |
|---|---|
| GET /health | Working |
| GET /ready | Working |
| GET /metrics | Working |
| POST /predict | Working |
| POST /recommend | Working |
| GET /movies/{movie_id} | Working |

## Validation Commands

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test
```

## Current Capability

Lumina Rec can:

- Train a MovieLens recommender
- Log model artifacts to MLflow
- Store artifacts in MinIO
- Use Postgres as the MLflow backend
- Load approved artifacts by run ID
- Verify model checksum
- Serve rating predictions
- Serve top N recommendations
- Return movie title and genre metadata in recommendations
- Run API tests
- Run load tests
- Document operations, security, testing, rollback, and promotion

## Latest Completed Build Task

Added movie title and genre metadata to `/recommend` responses.

## Next Build Task

Add `/movies/{movie_id}` lookup endpoint.