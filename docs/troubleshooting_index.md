# Troubleshooting Index

## Purpose

This file points to troubleshooting resources.

## Common Problems

| Problem | Start Here |
|---|---|
| Inference not ready | docs/incident_response_runbook.md |
| Wrong model loaded | docs/model_rollback_procedure.md |
| MLflow not reachable | docs/runbook_quickstart.md |
| MinIO bucket missing | scripts/create_minio_bucket.ps1 |
| Tests failing | docs/testing_strategy.md |
| Docker issues | docs/docker_cleanup.md |
| Bad API key | docs/api_security_plan.md |
| Checksum failure | docs/model_rollback_procedure.md |
| Unknown movie or user | docs/data_dictionary.md |
| Git confusion | docs/git_workflow.md |

## First Commands To Run

```powershell
docker compose ps
docker compose logs inference --tail=120
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 test
git status