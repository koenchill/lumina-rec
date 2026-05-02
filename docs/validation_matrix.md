# Validation Matrix

## Purpose

This file maps validation checks to commands and expected outcomes.

| Area | Command | Expected Result |
|---|---|---|
| Health | `.\scripts\lumina.ps1 health` | status ok |
| Readiness | `.\scripts\lumina.ps1 ready` | approved model metadata |
| Prediction | `.\scripts\lumina.ps1 predict` | predicted rating response |
| Recommendation | `.\scripts\lumina.ps1 recommend` | recommendations response |
| Movie lookup | `.\scripts\lumina.ps1 movie` | movie title and genres |
| Metrics | `.\scripts\lumina.ps1 metrics` | Prometheus metrics |
| Tests | `.\scripts\lumina.ps1 test` | all tests pass |
| Load test | `.\scripts\lumina.ps1 load-test` | 0 failures |
| MLflow | `Invoke-WebRequest -Uri http://localhost:5000 -UseBasicParsing` | StatusCode 200 |
| MinIO bucket | `docker compose exec minio mc ls local` | mlflow-artifacts exists |

## Release Gate

Before closing a work session, run:

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 test
git status