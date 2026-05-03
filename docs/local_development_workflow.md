# Local Development Workflow

## Purpose

This document defines the normal local development workflow for Lumina Rec.

## Standard Workflow

1. Start Docker Desktop.
2. Activate Python virtual environment.
3. Start required services.
4. Make code or documentation changes.
5. Validate locally.
6. Commit changes.
7. Push to GitHub.

## Commands

### Start services

```powershell
docker compose up -d postgres minio mlflow
docker compose up -d --build inference