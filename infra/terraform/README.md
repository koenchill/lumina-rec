# Terraform

## Purpose

Infrastructure as code for Lumina Rec local/dev packaging.

Current target: manage the **Kubernetes inference** workload (and model registry
metadata ConfigMap) against Docker Desktop Kubernetes, while MLflow/MinIO/Postgres
remain on Docker Compose.

## Structure

```text
terraform/
├── environments/
│   └── dev/
└── modules/
    ├── inference_service/
    └── model_registry/
```

## Prerequisites

1. Terraform CLI installed (`terraform version`).
2. Docker Desktop Kubernetes running (`kubectl get nodes`).
3. Compose deps up: `postgres`, `minio`, `mlflow`.
4. Local image `lumina-rec-inference:latest`.
5. Repo-root `.env` with valid `MODEL_RUN_ID` / `MODEL_SHA256`.

## Quick start

```powershell
# Optional: remove resources previously created by scripts/k8s.ps1
.\scripts\k8s.ps1 down

# Create local terraform.tfvars from .env (gitignored)
.\scripts\terraform.ps1 write-tfvars

.\scripts\terraform.ps1 init
.\scripts\terraform.ps1 plan
.\scripts\terraform.ps1 apply
```

Expose and validate:

```powershell
kubectl -n lumina-rec port-forward svc/inference 8002:8000
curl.exe http://localhost:8002/ready
```

## Destroy / switch back to kubectl helper

```powershell
.\scripts\terraform.ps1 destroy
.\scripts\k8s.ps1 deploy
```

## Notes

- Do **not** commit `terraform.tfvars` (secrets / model pins; gitignored).
- Do commit `.terraform.lock.hcl` for reproducible provider versions.
- If winget installed Terraform but `terraform` is missing in a new shell, refresh
  PATH or reopen the terminal.
- This stack is **local/dev only** (Docker Desktop Kubernetes). Cloud roots are future work.
