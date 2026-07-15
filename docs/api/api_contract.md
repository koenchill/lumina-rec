# API Contract

## Purpose

This document defines the Lumina Rec API contract for local inference, recommendation, metadata lookup, readiness, metrics, model metadata, and error responses.

## Base URL

```text
http://localhost:8001
```

## Endpoint Summary

| Method | Endpoint | API Key Required | Purpose |
|---|---|---|---|
| GET | /health | No | Confirms the API process is running |
| GET | /ready | No | Confirms the approved model is loaded and ready |
| GET | /version | No | Returns service and model version metadata |
| GET | /model | No | Returns current approved model serving metadata |
| GET | /metrics | No | Returns Prometheus metrics |
| GET | /movies/{movie_id} | No | Returns movie title and genre metadata |
| POST | /predict | Yes | Predicts a rating for one user and movie |
| POST | /recommend | Yes | Returns top N recommendations for a user |

## Authentication

Protected endpoints require this header:

```http
x-api-key: local-dev-api-key
```

Protected endpoints:

| Endpoint | Required Header |
|---|---|
| POST /predict | x-api-key |
| POST /recommend | x-api-key |

## GET /health

### Request

```http
GET /health
```

### Success Response

```json
{
  "status": "ok"
}
```

## GET /ready

### Request

```http
GET /ready
```

### Success Response

```json
{
  "status": "ready",
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0",
  "model_run_id": "5248dddd8e97477da7651507b418d989",
  "model_artifact_path": "approved_model",
  "model_sha256": "79d2b50837a3af983530db10179e46ae7f26c7467d8fed31cc2f1fa9804cc97d",
  "checksum_validation": "enabled",
  "model_registry_enabled": "true",
  "registered_model_name": "lumina-rec-movielens-mf",
  "model_alias": "approved",
  "movie_metadata_status": "loaded",
  "movie_metadata_count": "9742",
  "artifact_manifest_status": "validated",
  "artifact_manifest_version": "1.0"
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| status | string | Readiness status |
| model_name | string | Current approved model name |
| model_version | string | Current approved model version |
| model_run_id | string | Resolved MLflow run ID |
| model_artifact_path | string | MLflow artifact path used by inference |
| model_sha256 | string | SHA256 checksum of the loaded model |
| checksum_validation | string | Whether model checksum validation is enabled |
| model_registry_enabled | string | Whether MLflow registry alias loading is enabled |
| registered_model_name | string | MLflow registered model name |
| model_alias | string | MLflow alias used for approved serving |
| movie_metadata_status | string | Movie metadata loading status |
| movie_metadata_count | string | Count of loaded movie metadata records |
| artifact_manifest_status | string | Artifact manifest validation status |
| artifact_manifest_version | string | Artifact manifest schema version |

## GET /version

### Request

```http
GET /version
```

### Success Response

```json
{
  "service_name": "lumina-rec-inference",
  "service_version": "0.2.0",
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0"
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| service_name | string | Inference service name |
| service_version | string | Inference service version |
| model_name | string | Current approved model name |
| model_version | string | Current approved model version |

## GET /model

### Request

```http
GET /model
```

### Success Response

```json
{
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0",
  "model_run_id": "5248dddd8e97477da7651507b418d989",
  "model_artifact_path": "approved_model",
  "model_sha256": "79d2b50837a3af983530db10179e46ae7f26c7467d8fed31cc2f1fa9804cc97d",
  "checksum_validation": "enabled",
  "artifact_manifest_status": "validated",
  "artifact_manifest_version": "1.0",
  "model_registry_enabled": "true",
  "registered_model_name": "lumina-rec-movielens-mf",
  "model_alias": "approved"
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| model_name | string | Current approved model name |
| model_version | string | Current approved model version |
| model_run_id | string | Resolved MLflow run ID |
| model_artifact_path | string | MLflow artifact path used by inference |
| model_sha256 | string | SHA256 checksum of the loaded model |
| checksum_validation | string | Whether checksum validation is enabled |
| artifact_manifest_status | string | Artifact manifest validation status |
| artifact_manifest_version | string | Artifact manifest schema version |
| model_registry_enabled | string | Whether registry alias loading is enabled |
| registered_model_name | string | MLflow registered model name |
| model_alias | string | MLflow model alias used for approved serving |

## GET /metrics

### Request

```http
GET /metrics
```

### Success Response

```text
# HELP lumina_prediction_requests_total Total number of prediction and recommendation requests
# TYPE lumina_prediction_requests_total counter
```

### Current Metrics

| Metric | Purpose |
|---|---|
| lumina_prediction_requests_total | Counts successful prediction and recommendation requests |
| lumina_prediction_errors_total | Counts failed prediction and recommendation requests |
| lumina_prediction_latency_ms | Tracks prediction and recommendation latency |
| lumina_rate_limit_errors_total | Counts rate limited requests |

## GET /movies/{movie_id}

### Request

```http
GET /movies/1
```

### Success Response

```json
{
  "movie_id": 1,
  "title": "Toy Story (1995)",
  "genres": "Adventure|Animation|Children|Comedy|Fantasy"
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| movie_id | integer | MovieLens movie ID |
| title | string | Movie title from `movies_metadata.csv` |
| genres | string | Pipe separated MovieLens genres |

### Error Response

If the movie does not exist in the approved MovieLens metadata, the API returns:

```json
{
  "detail": {
    "error_code": "UNKNOWN_MOVIE_ID",
    "detail": "Unknown movie_id: 999999999",
    "request_id": null
  }
}
```

## POST /predict

### Request

```http
POST /predict
Content-Type: application/json
x-api-key: local-dev-api-key
```

### Request Body

```json
{
  "user_id": 1,
  "movie_id": 1
}
```

### Request Rules

| Field | Type | Rule |
|---|---|---|
| user_id | integer | Must exist in the approved MovieLens user mapping |
| movie_id | integer | Must exist in the approved MovieLens movie mapping |

### Success Response

```json
{
  "predicted_rating": 5.0,
  "user_id": 1,
  "movie_id": 1,
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0",
  "request_id": "example-request-id",
  "latency_ms": 45.91
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| predicted_rating | float | Predicted rating from 0.5 to 5.0 |
| user_id | integer | Requested MovieLens user ID |
| movie_id | integer | Requested MovieLens movie ID |
| model_name | string | Current approved model name |
| model_version | string | Current approved model version |
| request_id | string | Request trace ID |
| latency_ms | float | Request processing time in milliseconds |

### Error Responses

| Condition | Error Code | Status |
|---|---|---:|
| Missing API key | AUTH_INVALID_API_KEY | 401 |
| Invalid API key | AUTH_INVALID_API_KEY | 401 |
| Missing required field | FastAPI validation error | 422 |
| Unknown user_id | UNKNOWN_USER_ID | 404 |
| Unknown movie_id | UNKNOWN_MOVIE_ID | 404 |
| Rate limit exceeded | RATE_LIMIT_EXCEEDED | 429 |
| Internal prediction failure | PREDICTION_FAILED | 500 |

## POST /recommend

### Request

```http
POST /recommend
Content-Type: application/json
x-api-key: local-dev-api-key
```

### Request Body

```json
{
  "user_id": 1,
  "top_n": 10
}
```

### Request Rules

| Field | Type | Rule |
|---|---|---|
| user_id | integer | Must exist in the approved MovieLens user mapping |
| top_n | integer | Optional. Defaults to 10. Must be between 1 and 50 |

### Success Response

```json
{
  "user_id": 1,
  "recommendations": [
    {
      "movie_id": 1,
      "title": "Toy Story (1995)",
      "genres": "Adventure|Animation|Children|Comedy|Fantasy",
      "predicted_rating": 5.0
    },
    {
      "movie_id": 2,
      "title": "Jumanji (1995)",
      "genres": "Adventure|Children|Fantasy",
      "predicted_rating": 5.0
    }
  ],
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0",
  "request_id": "example-request-id",
  "latency_ms": 11.55
}
```

### Recommendation Item Fields

| Field | Type | Description |
|---|---|---|
| movie_id | integer | Recommended MovieLens movie ID |
| title | string | Movie title from `movies_metadata.csv` |
| genres | string | Pipe separated MovieLens genres |
| predicted_rating | float | Predicted rating for the recommended movie |

### Error Responses

| Condition | Error Code | Status |
|---|---|---:|
| Missing API key | AUTH_INVALID_API_KEY | 401 |
| Invalid API key | AUTH_INVALID_API_KEY | 401 |
| Missing user_id | FastAPI validation error | 422 |
| Invalid top_n | FastAPI validation error | 422 |
| Unknown user_id | UNKNOWN_USER_ID | 404 |
| Rate limit exceeded | RATE_LIMIT_EXCEEDED | 429 |
| Internal recommendation failure | RECOMMENDATION_FAILED | 500 |

## Structured Error Response

Protected and known business error responses use a structured error body.

### Error Shape

```json
{
  "detail": {
    "error_code": "UNKNOWN_MOVIE_ID",
    "detail": "Unknown movie_id: 999999999",
    "request_id": "example-request-id"
  }
}
```

### Error Fields

| Field | Type | Description |
|---|---|---|
| error_code | string | Stable machine readable error code |
| detail | string | Human readable error message |
| request_id | string or null | Request trace ID when available |

### Current Error Codes

| Error Code | Status | Meaning |
|---|---:|---|
| AUTH_INVALID_API_KEY | 401 | Missing or invalid API key |
| UNKNOWN_USER_ID | 404 | User ID does not exist in approved mappings |
| UNKNOWN_MOVIE_ID | 404 | Movie ID does not exist in approved mappings or metadata |
| RATE_LIMIT_EXCEEDED | 429 | Caller exceeded configured rate limit |
| MODEL_NOT_LOADED | 503 | Model is unavailable |
| PREDICTION_FAILED | 500 | Prediction failed |
| RECOMMENDATION_FAILED | 500 | Recommendation failed |

FastAPI schema validation errors still return the default 422 response shape.