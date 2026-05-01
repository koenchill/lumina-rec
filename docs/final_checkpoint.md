# Final Checkpoint

## Project

Lumina Rec

## Status

The local MLOps recommendation system is working and documented.

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

## Validation Commands

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test