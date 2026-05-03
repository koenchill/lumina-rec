# Recommendation API

## Purpose

This document explains the Lumina Rec recommendation API, prediction API, movie metadata lookup, service metadata endpoints, and structured errors.

## Base URL

```text
http://localhost:8001
```

## Endpoint Summary

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Confirms the API process is running |
| GET | /ready | Confirms the approved model is loaded and ready |
| GET | /version | Returns service and model version metadata |
| GET | /model | Returns current approved model serving metadata |
| GET | /metrics | Returns Prometheus metrics |
| GET | /movies/{movie_id} | Returns movie title and genre metadata |
| POST | /predict | Predicts a rating for one user and movie |
| POST | /recommend | Returns top N recommendations for a user |

## Authentication

The following endpoints require an API key:

| Endpoint | Header |
|---|---|
| POST /predict | x-api-key |
| POST /recommend | x-api-key |

Example:

```http
x-api-key: local-dev-api-key
```

## Service Metadata Endpoints

### GET /version

```http
GET /version
```

Example response:

```json
{
  "service_name": "lumina-rec-inference",
  "service_version": "0.2.0",
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0"
}
```

### GET /model

```http
GET /model
```

Example response:

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

## GET /movies/{movie_id}

### Request

```http
GET /movies/1
```

### Response

```json
{
  "movie_id": 1,
  "title": "Toy Story (1995)",
  "genres": "Adventure|Animation|Children|Comedy|Fantasy"
}
```

### Error Example

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

### Common Errors

| Error Code | Status | Meaning |
|---|---:|---|
| AUTH_INVALID_API_KEY | 401 | Missing or invalid API key |
| UNKNOWN_USER_ID | 404 | User ID does not exist in approved mappings |
| UNKNOWN_MOVIE_ID | 404 | Movie ID does not exist in approved mappings |
| RATE_LIMIT_EXCEEDED | 429 | Caller exceeded configured rate limit |
| PREDICTION_FAILED | 500 | Prediction failed |

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

### Common Errors

| Error Code | Status | Meaning |
|---|---:|---|
| AUTH_INVALID_API_KEY | 401 | Missing or invalid API key |
| UNKNOWN_USER_ID | 404 | User ID does not exist in approved mappings |
| RATE_LIMIT_EXCEEDED | 429 | Caller exceeded configured rate limit |
| RECOMMENDATION_FAILED | 500 | Recommendation failed |

## Structured Errors

Known API errors return this shape:

```json
{
  "detail": {
    "error_code": "AUTH_INVALID_API_KEY",
    "detail": "Invalid or missing API key",
    "request_id": "example-request-id"
  }
}
```

| Error Code | Status | Applies To |
|---|---:|---|
| AUTH_INVALID_API_KEY | 401 | `/predict`, `/recommend` |
| UNKNOWN_USER_ID | 404 | `/predict`, `/recommend` |
| UNKNOWN_MOVIE_ID | 404 | `/predict`, `/movies/{movie_id}` |
| RATE_LIMIT_EXCEEDED | 429 | `/predict`, `/recommend` |
| MODEL_NOT_LOADED | 503 | `/ready` |
| PREDICTION_FAILED | 500 | `/predict` |
| RECOMMENDATION_FAILED | 500 | `/recommend` |

FastAPI schema validation errors still return the default 422 response shape.

## Validation Commands

.\scripts\lumina.ps1 ready
Invoke-RestMethod -Uri http://localhost:8001/version -Method Get
Invoke-RestMethod -Uri http://localhost:8001/model -Method Get
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 test
