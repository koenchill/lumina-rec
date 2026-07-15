# Disaster Recovery Plan

## Purpose

This document defines recovery planning for Lumina Rec.

## Recovery Scenarios

| Scenario | Recovery Action |
|---|---|
| Inference container fails | Rebuild and restart inference |
| Wrong model deployed | Roll back MODEL_RUN_ID and MODEL_SHA256 |
| MLflow unavailable | Restart MLflow, Postgres, and MinIO |
| MinIO bucket missing | Recreate `mlflow-artifacts` bucket |
| Model artifact missing | Restore from MLflow artifact store or retrain |
| Local Docker failure | Restart Docker Desktop |

## Recovery Commands

```powershell
docker compose ps
docker compose logs inference --tail=120
docker compose up -d postgres minio mlflow
docker compose up -d --build inference
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 test