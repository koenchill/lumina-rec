# Container Security Plan

## Purpose

This document defines the container security plan for Lumina Rec.

## Current Container

| Component | Value |
|---|---|
| Service | inference |
| Base image | python:3.11-slim |
| Framework | FastAPI |
| Model runtime | PyTorch CPU |

## Current Controls

| Control | Status |
|---|---|
| Slim base image | Implemented |
| CPU only PyTorch | Implemented |
| Dockerfile under version control | Implemented |
| Trivy scan | Implemented |
| Secrets excluded from image | Expected |
| Runtime env variables | Implemented |

## Future Controls

| Control | Purpose |
|---|---|
| Non root container user | Reduce privilege risk |
| Read only filesystem | Reduce write surface |
| Image signing | Improve supply chain assurance |
| SBOM generation | Track image contents |
| Critical vulnerability gate | Block risky builds |
| Minimal runtime packages | Reduce attack surface |

## Validation Commands

```powershell
docker compose build inference
docker compose up -d inference
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 test