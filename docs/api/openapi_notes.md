# OpenAPI Notes

## Purpose

FastAPI automatically exposes OpenAPI documentation for Lumina Rec.

## Local URLs

| URL | Purpose |
|---|---|
| http://localhost:8001/docs | Swagger UI |
| http://localhost:8001/redoc | ReDoc |
| http://localhost:8001/openapi.json | OpenAPI schema |

## Current API Areas

- Health checks
- Readiness checks
- Metrics
- Movie metadata lookup
- Rating prediction
- Top N recommendations

## Future Work

- Export OpenAPI schema to this folder
- Add API versioning
- Add structured error response models
- Add auth documentation for production