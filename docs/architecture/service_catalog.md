# Service Catalog

## Purpose

This file lists the local services used by Lumina Rec.

## Services

| Service | Purpose | Port |
|---|---|---|
| inference | FastAPI inference service | 8001 |
| mlflow | Experiment tracking and artifact metadata | 5000 |
| minio | Local S3 compatible artifact storage | 9000, 9001 |
| postgres | MLflow backend metadata store | 5433 |
| redis | Future cache placeholder | 6379 |
| keycloak | Future identity provider placeholder | 8082 |
| localstack | Future AWS local development placeholder | 4566 |

## Core Services Required

| Service | Required For |
|---|---|
| inference | API serving |
| mlflow | Approved artifact lookup |
| minio | Artifact storage |
| postgres | MLflow backend store |

## Optional Services

| Service | Future Use |
|---|---|
| redis | Cache and queue workflows |
| keycloak | Identity and JWT testing |
| localstack | Local AWS service testing |