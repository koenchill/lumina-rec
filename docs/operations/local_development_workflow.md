# Local Development Workflow

## Purpose

This document defines the normal local development workflow for Lumina Rec.

## Standard Workflow

1. Start Docker Desktop.
2. Activate Python virtual environment.
3. Start required services.
4. Make code or documentation changes.
5. Validate locally.
6. Commit changes.
7. Push to GitHub.

## Commands

### Start services

```powershell
.\scripts\lumina.ps1 up
# equivalent: docker compose up -d --build
```

Optional placeholders:

```powershell
docker compose --profile extras up -d
```

If inference cannot load the pinned model run, train into local MLflow and update
`.env` from `reports/latest_training_run.json`, then recreate inference.

### Validate

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test
```
