# Infrastructure

## Purpose

This folder holds infrastructure for packaging and deploying Lumina Rec.

The application itself is treated as a stable training target. Infra work focuses on
**Docker → Kubernetes → Terraform**, in that order.

## Current State

| Layer | Status |
|---|---|
| Docker Compose (local core stack) | Done — primary local runtime |
| Inference Dockerfile | Done — `services/inference/Dockerfile` |
| Kubernetes | Not started |
| Terraform | Placeholder folders only (no `.tf` yet) |

## Local Docker Stack (core)

Default `docker compose up` starts only the services needed to train/serve:

| Service | Purpose | Host |
|---|---|---|
| `inference` | FastAPI serving | http://localhost:8001 |
| `mlflow` | Tracking + artifact metadata | http://localhost:5000 |
| `minio` | S3-compatible artifact store | http://localhost:9000 (console :9001) |
| `minio-init` | Creates `mlflow-artifacts` bucket | one-shot |
| `postgres` | MLflow backend store | localhost:5433 |

Optional placeholders (Redis, Keycloak, LocalStack):

```powershell
docker compose --profile extras up -d
```

### Image sources

Compose avoids flaky Docker Hub CDN pulls where possible:

| Image | Source |
|---|---|
| MinIO server / client | `quay.io/minio/...` |
| Postgres 16 | `mirror.gcr.io/library/postgres:16` |
| MLflow | `ghcr.io/mlflow/mlflow:v2.12.2` |

### Bring-up

1. Copy `.env.example` to `.env`.
2. Start Docker Desktop.
3. Bring up the stack:

```powershell
.\scripts\lumina.ps1 up
# or
docker compose up -d --build
```

4. If inference stays unhealthy with `RESOURCE_DOES_NOT_EXIST` for `MODEL_RUN_ID`,
   train into this local MLflow instance and pin the new run:

```powershell
$env:PYTHONPATH = "src;."
.\.venv\Scripts\python.exe .\ml\training\train.py
# Copy model_run_id and model_sha256 from reports/latest_training_run.json into .env
docker compose up -d --force-recreate inference
```

5. Confirm readiness:

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
```

`MODEL_RUN_ID` and `MODEL_SHA256` are required. They must exist in the **current**
local MLflow/MinIO volume data (a fresh Postgres volume invalidates old pins).

Do not leave shell overrides like `$env:MODEL_RUN_ID` set; Compose prefers the shell
environment over `.env`.

CI validates image build + Compose config. Full `/ready` serving checks are local.

## Training Roadmap (infra)

1. **Docker** — Harden image/Compose/CI (**done**)
2. **Kubernetes** — Deploy the same inference image locally (Kind/k3d)
3. **Terraform** — Codify a `dev` environment under `infra/terraform/`

## Planned Folders

| Folder | Purpose |
|---|---|
| terraform | Infrastructure as code |
| terraform/environments | Environment-specific settings |
| terraform/modules | Reusable modules (`inference_service`, `model_registry`) |

## Future Production Target

- Containerized inference service
- Managed object storage for model artifacts
- Managed Postgres for metadata
- Managed secrets
- API gateway authentication
- TLS
- Centralized logs and metrics
- Network segmentation
