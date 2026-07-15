# Infrastructure

## Purpose

This folder holds infrastructure for packaging and deploying Lumina Rec.

The application is treated as a stable training target. Local infra follows
**Docker → Kubernetes → Terraform**.

## Current State

| Layer | Status |
|---|---|
| Docker Compose (local core stack) | Done — MLflow / MinIO / Postgres (+ optional Compose inference) |
| Inference Dockerfile | Done — `services/inference/Dockerfile` |
| Kubernetes | Done — inference manifests + `scripts/k8s.ps1` |
| Terraform | Done for local/dev — preferred owner of the K8s inference workload |

**Ownership:** use **Terraform** (`scripts/terraform.ps1`) to create/update the
Kubernetes inference deployment. Keep `scripts/k8s.ps1` / `infra/k8s` as a manual
kubectl/kustomize fallback. Do not apply both against the same namespace without
tearing one down first.

## Local Docker Stack (core)

Default `docker compose up` starts:

| Service | Purpose | Host |
|---|---|---|
| `inference` | FastAPI serving (Compose path) | http://localhost:8001 |
| `mlflow` | Tracking + artifact metadata | http://localhost:5000 |
| `minio` | S3-compatible artifact store | http://localhost:9000 (console :9001) |
| `minio-init` | Creates `mlflow-artifacts` bucket | one-shot |
| `postgres` | MLflow backend store | localhost:5433 |

Optional placeholders:

```powershell
docker compose --profile extras up -d
```

### Image sources

| Image | Source |
|---|---|
| MinIO server / client | `quay.io/minio/...` |
| Postgres 16 | `mirror.gcr.io/library/postgres:16` |
| MLflow | `ghcr.io/mlflow/mlflow:v2.12.2` |

### Compose bring-up

1. Copy `.env.example` to `.env` and set a valid model pin.
2. Start Docker Desktop.
3. Bring up the stack:

```powershell
.\scripts\lumina.ps1 up
```

4. If inference reports `RESOURCE_DOES_NOT_EXIST` for `MODEL_RUN_ID`, train and re-pin:

```powershell
$env:PYTHONPATH = "src;."
.\.venv\Scripts\python.exe .\ml\training\train.py
# Copy model_run_id / model_sha256 from reports/latest_training_run.json into .env
docker compose up -d --force-recreate inference
```

5. Validate:

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
```

`MODEL_RUN_ID` and `MODEL_SHA256` must exist in the **current** local MLflow/MinIO
volumes. Clear accidental shell overrides (`$env:MODEL_RUN_ID`) before Compose.

## Local Kubernetes + Terraform (inference)

Compose still runs MLflow / MinIO / Postgres. Kubernetes runs inference and reaches
those services at `host.docker.internal`.

**Preferred path (Terraform):**

```powershell
docker compose up -d postgres minio minio-init mlflow
.\scripts\terraform.ps1 write-tfvars
.\scripts\terraform.ps1 init
.\scripts\terraform.ps1 apply
kubectl -n lumina-rec port-forward svc/inference 8002:8000
curl.exe http://localhost:8002/ready
```

**Fallback path (kubectl/kustomize):**

```powershell
.\scripts\k8s.ps1 down    # if Terraform currently owns the namespace
.\scripts\k8s.ps1 deploy
kubectl -n lumina-rec port-forward svc/inference 8002:8000
```

| Path | Inference URL |
|---|---|
| Compose | http://localhost:8001 |
| Kubernetes (port-forward) | http://localhost:8002 |

Details:

- [`k8s/README.md`](k8s/README.md)
- [`terraform/README.md`](terraform/README.md)

## Training Roadmap (infra)

1. **Docker** — Compose + image + CI (**done**)
2. **Kubernetes** — Local inference Deployment (**done**)
3. **Terraform** — Local/dev Kubernetes IaC (**done**)

## Folders

| Folder | Purpose |
|---|---|
| `k8s/` | Manifests + manual deploy helper |
| `terraform/` | IaC root |
| `terraform/environments/dev/` | Docker Desktop root module |
| `terraform/modules/` | `inference_service`, `model_registry` |

## Future Production Target

- Managed object storage and Postgres
- Managed secrets, TLS, API gateway
- Centralized logs/metrics
- Cloud environment roots beyond local Kubernetes
