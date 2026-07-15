# Inference Service Module

## Purpose

Deploys the Lumina Rec inference API to Kubernetes.

## Responsibilities

- Create namespace (optional)
- Create inference Secret and ConfigMap
- Deploy FastAPI container with health/readiness probes
- Expose ClusterIP Service

## Required inputs

| Variable | Purpose |
|---|---|
| `namespace` | Target namespace |
| `image` | Inference image |
| `mlflow_tracking_uri` | MLflow URL from the pod |
| `mlflow_s3_endpoint_url` | MinIO/S3 endpoint from the pod |
| `model_run_id` / `model_sha256` | Approved model pin |
| `lumina_api_key` | API authentication key |

## Current status

Implemented for local Docker Desktop Kubernetes + Compose artifact stack.
