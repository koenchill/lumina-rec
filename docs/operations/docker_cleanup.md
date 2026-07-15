# Docker Cleanup Notes

## Purpose

This note explains how to safely clean Docker Desktop clutter without removing the running Lumina Rec stack.

## Current Core Services

The core services are:

- inference
- mlflow
- postgres
- minio
- minio-init (one-shot bucket bootstrap)

Optional local services (Compose profile `extras`) are:

- redis
- keycloak
- localstack

Start optional services with:

```powershell
docker compose --profile extras up -d
```

## Safe Cleanup

### Show all containers

```powershell
docker ps -a
```

### Remove stopped containers only

```powershell
docker container prune
```

Type `y` when prompted.

This removes stopped containers only. It does not remove running Lumina Rec services.

### Confirm Lumina services are still running

```powershell
docker compose ps
```

Expected core services:

```text
inference
mlflow
postgres
minio
```

### Check Docker disk usage

```powershell
docker system df
```

## Optional Cleanup

### Remove unused networks, dangling images, and build cache

```powershell
docker system prune
```

Type `y` when prompted.

## Avoid Unless Needed

Do not run this during normal cleanup:

```powershell
docker system prune -a
```

This removes unused images and may force large rebuilds later.

## Validate After Cleanup

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
```

Expected result:

- `/ready` returns approved model metadata
- `/predict` returns rating prediction metadata
- `/recommend` returns recommendation metadata

## Files Not To Commit

```text
.env
.venv/
ml/models/approved/
tests/load/load_test_report.html
__pycache__/
*.pyc
```