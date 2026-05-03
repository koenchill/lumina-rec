# Backup and Restore Plan

## Purpose

This document defines future backup and restore needs for Lumina Rec.

## Backup Targets

| Asset | Why It Matters |
|---|---|
| MLflow metadata | Tracks experiments and model runs |
| MinIO artifacts | Stores approved model artifacts |
| `.env` values | Defines local approved runtime state |
| Documentation | Supports operations and handoff |
| Source code | Defines application behavior |

## Local Development Approach

For local development:

- Source code is backed up through Git.
- Model artifacts are reproducible through training.
- Approved run metadata is documented.
- `.env` is not committed and should be recreated from `.env.example`.

## Future Production Approach

| Asset | Target Backup |
|---|---|
| Postgres | Managed database snapshots |
| Object storage | Bucket versioning and lifecycle policy |
| Secrets | Managed secret backup and rotation policy |
| Container images | Container registry retention |
| Logs | Centralized logging retention |

## Restore Validation

After restore, run:

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 test