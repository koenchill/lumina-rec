# Access Control Matrix

## Purpose

This document defines current and future access expectations for Lumina Rec.

## Current Local Access

| Resource | Access Method | Current Control |
|---|---|---|
| `/predict` | API request | API key |
| `/recommend` | API request | API key |
| `/movies/{movie_id}` | API request | Open locally |
| `/health` | API request | Open locally |
| `/ready` | API request | Open locally |
| `/metrics` | API request | Open locally |
| MLflow UI | Browser | Open locally |
| MinIO console | Browser | Local credentials |
| Postgres | Local port | Local credentials |

## Future Production Access

| Resource | Target Control |
|---|---|
| Prediction API | JWT or API gateway |
| Recommendation API | JWT or API gateway |
| Metrics | Internal monitoring only |
| MLflow | Authenticated admin access |
| Artifact storage | Least privilege service role |
| Postgres | Private network and managed identity |
| Secrets | Managed secret store |

## Access Review Questions

- Who can call inference endpoints?
- Who can promote a model?
- Who can change runtime secrets?
- Who can view model artifacts?
- Who can access logs and metrics?