# FAQ

## What is Lumina Rec?

Lumina Rec is a local MLOps recommendation system built around MovieLens, MLflow, MinIO, Postgres, FastAPI, Docker Compose, Pytest, and Locust.

## What does it demonstrate?

It demonstrates model training, experiment tracking, artifact storage, approved model loading, checksum validation, API serving, testing, load testing, and documentation.

## What model does it use?

It uses a MovieLens matrix factorization recommender.

## What endpoints exist?

| Endpoint | Purpose |
|---|---|
| GET /health | Health check |
| GET /ready | Model readiness |
| GET /metrics | Prometheus metrics |
| GET /movies/{movie_id} | Movie metadata lookup |
| POST /predict | Rating prediction |
| POST /recommend | Top N recommendations |

## Why use MLflow?

MLflow tracks model runs, metrics, parameters, and artifacts.

## Why use MinIO?

MinIO provides local S3 compatible artifact storage.

## Why use SHA256?

SHA256 confirms the model artifact matches the approved file before inference starts.

## Is this production ready?

No. It is ready for local development and portfolio demonstration. Production would require stronger authentication, managed secrets, TLS, restricted metrics, centralized logs, and deployment hardening.