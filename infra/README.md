# Infrastructure

## Purpose

This folder stores future infrastructure assets for Lumina Rec.

## Current State

The project currently runs locally with Docker Compose.

## Future Target

The future infrastructure target should support:

- Containerized inference service
- Managed object storage for model artifacts
- Managed Postgres for metadata
- Managed secrets
- API gateway authentication
- TLS
- Centralized logs
- Centralized metrics
- Network segmentation

## Planned Folders

| Folder | Purpose |
|---|---|
| terraform | Future infrastructure as code |
| terraform/environments | Environment specific settings |
| terraform/modules | Reusable infrastructure modules |