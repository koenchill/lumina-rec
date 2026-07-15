# Kubernetes (local)

## Purpose

Run the Lumina Rec **inference** service on local Kubernetes while MLflow, MinIO,
and Postgres continue on Docker Compose.

## Prerequisites

1. Docker Desktop Kubernetes enabled (`kubectl get nodes` shows a Ready node).
2. Local `.env` with a valid `MODEL_RUN_ID` / `MODEL_SHA256` for the Compose MLflow stack.
3. Inference image available locally: `lumina-rec-inference:latest`.

## Architecture (training slice)

| Component | Where it runs |
|---|---|
| inference | Kubernetes (`lumina-rec` namespace) |
| mlflow / minio / postgres | Docker Compose on the host |
| Model pin + API key | Kubernetes Secret from `.env` |

Inference reaches host Compose services at:

- `http://host.docker.internal:5000` (MLflow)
- `http://host.docker.internal:9000` (MinIO)

Compose inference can stay on `:8001`. Kubernetes inference is exposed via port-forward on `:8002`.

## Deploy

```powershell
# Optional rebuild
.\scripts\k8s.ps1 build

# Apply manifests + secret from .env
.\scripts\k8s.ps1 deploy

# In a second terminal, expose the service
kubectl -n lumina-rec port-forward svc/inference 8002:8000
```

## Validate

```powershell
.\scripts\k8s.ps1 status
.\scripts\k8s.ps1 ready
curl.exe http://localhost:8002/health
curl.exe http://localhost:8002/ready
```

## Useful commands

```powershell
.\scripts\k8s.ps1 logs
.\scripts\k8s.ps1 restart
.\scripts\k8s.ps1 down
```

## Files

| File | Purpose |
|---|---|
| `namespace.yaml` | `lumina-rec` namespace |
| `configmap.yaml` | Non-secret runtime config |
| `deployment.yaml` | Inference Deployment + probes |
| `service.yaml` | ClusterIP Service |
| `kustomization.yaml` | Apply set |
| `kind-config.yaml` | Optional Kind cluster config (alternate to Docker Desktop) |
