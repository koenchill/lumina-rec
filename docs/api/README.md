# API Documentation

API contracts, examples, and OpenAPI notes for Lumina Rec.

The implementation lives in `services/inference/`. This folder is documentation only.

## Documents

| File | Purpose |
|---|---|
| [api_contract.md](api_contract.md) | Endpoints, headers, request/response shapes |
| [recommendation_api.md](recommendation_api.md) | `/predict`, `/recommend`, movie lookup |
| [error_handling_standard.md](error_handling_standard.md) | Safe API error behavior |
| [openapi_notes.md](openapi_notes.md) | OpenAPI notes |
| [examples/](examples/) | Sample JSON request/response payloads |

## Current Endpoints

| Endpoint | Purpose |
|---|---|
| GET /health | Service health |
| GET /ready | Model readiness |
| GET /metrics | Prometheus metrics |
| GET /version | Service/model version |
| GET /model | Serving model metadata |
| GET /movies/{movie_id} | Movie metadata lookup |
| POST /predict | Rating prediction |
| POST /recommend | Top N recommendations |
