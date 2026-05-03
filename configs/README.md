# Configuration Files

## Purpose

This folder stores non secret configuration baselines for Lumina Rec.

## Files

| File | Purpose |
|---|---|
| local.yaml | Local environment baseline |
| model_serving.yaml | Model serving configuration reference |
| security_baseline.yaml | Security control baseline |
| observability.yaml | Metrics and logging baseline |

## Rules

- Do not store secrets here.
- Do not store `.env` values that should remain private.
- Use this folder for safe defaults and documentation friendly configuration.