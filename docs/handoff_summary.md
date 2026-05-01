# Handoff Summary

## Purpose

This document summarizes the current Lumina Rec project state for handoff.

## Current State

Lumina Rec is a local MLOps recommendation system using:

- PyTorch
- MLflow
- MinIO
- Postgres
- FastAPI
- Docker Compose
- Pytest
- Locust

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Working Endpoints

| Endpoint | Purpose |
|---|---|
| GET /health | Service health |
| GET /ready | Model readiness |
| GET /metrics | Prometheus metrics |
| POST /predict | Rating prediction |
| POST /recommend | Top N recommendations |

## Working Commands

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 load-test