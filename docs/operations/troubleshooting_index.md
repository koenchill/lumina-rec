# Troubleshooting Index

## Purpose

This file points to troubleshooting resources.

## Common Problems

| Problem | Start Here |
|---|---|
| Inference not ready | docs/operations/incident_response_runbook.md |
| Wrong model loaded | docs/mlops/model_rollback_procedure.md |
| MLflow not reachable | docs/operations/runbook_quickstart.md |
| MinIO bucket missing | scripts/create_minio_bucket.ps1 |
| Tests failing | docs/mlops/testing_strategy.md |
| Docker issues | docs/operations/docker_cleanup.md |
| Bad API key | docs/plans/api_security_plan.md |
| Checksum failure | docs/mlops/model_rollback_procedure.md |
| Unknown movie or user | docs/architecture/data_dictionary.md |
| Git confusion | docs/operations/git_workflow.md |

## First Commands To Run

```powershell
docker compose ps
docker compose logs inference --tail=120
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 test
git status