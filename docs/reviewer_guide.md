# Lumina Rec Reviewer Guide

## Purpose

This guide helps a reviewer validate the Lumina Rec local MLOps stack quickly.

## What This Project Shows

Lumina Rec demonstrates a local production shaped MLOps backend with:

- Model training
- MLflow tracking
- MinIO artifact storage
- Postgres metadata storage
- FastAPI inference
- API key authentication
- Rate limiting
- Model checksum validation
- Prometheus metrics
- Structured logs
- Docker Compose orchestration
- Automated tests
- Load testing
- CI security checks

## Start Here

Read these files first:

| File | Why It Matters |
|---|---|
| README.md | Project overview and common commands |
| docs/architecture.md | Architecture diagram and service flow |
| docs/api_contract.md | API endpoints and expected responses |
| docs/local_validation.md | Evidence the stack works |
| docs/security_controls.md | Implemented controls and risk reduction |
| docs/threat_model.md | Security risks and planned controls |

## Quick Validation

Run:

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 test