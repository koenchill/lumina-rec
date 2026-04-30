# Lumina Rec Inference API Contract

## Base URL

Local:

```text
http://localhost:8001
```

## Authentication

The `/predict` and `/recommend` endpoints require an API key.

Required header:

```http
x-api-key: local-dev-api-key
```

Health, readiness, and metrics endpoints do not require an API key in the local development setup.

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Endpoints

| Method | Endpoint | Authentication | Purpose |
|---|---|---|---|
| GET | /health | No | Confirms the API process is running |
| GET | /ready | No | Confirms the approved model artifact is loaded |
| GET | /metrics | No | Exposes Prometheus style metrics |
| POST | /predict | Yes | Returns a MovieLens rating prediction |
| POST | /recommend | Yes | Returns top N recommendations for a user |

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
  "model_run_id": "14eda4cf03bd4d328a3ee791ec9a002f",
  "model_artifact_path": "approved_model",
  "model_sha256": "205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd",
  "checksum_validation": "enabled"
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
  "latency_ms": 0.67
}
```

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
      "movie_id": 2,
      "predicted_rating": 5.0
    },
    {
      "movie_id": 3,
      "predicted_rating": 5.0
    }
  ],
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0",
  "request_id": "example-request-id",
  "latency_ms": 3.83
}
```

## Authentication Error

If the API key is missing or incorrect, the API returns:

```text
401 Unauthorized
```

Example response:

```json
{
  "detail": "Invalid or missing API key"
}
```

## Validation Error

If a required field is missing or `top_n` is outside the allowed range, the API returns:

```text
422 Unprocessable Entity
```

## Unknown User or Movie

If the user or movie does not exist in the approved MovieLens mapping, the API returns:

```text
404 Not Found
```

Example response:

```json
{
  "detail": "Unknown user_id: 999999999"
}
```

```json
{
  "detail": "Unknown movie_id: 999999999"
}
```

## GET /metrics

### Request

```http
GET /metrics
```

### Expected Metrics

```text
lumina_prediction_requests_total
lumina_prediction_errors_total
lumina_prediction_latency_ms
lumina_rate_limit_errors_total
```

## Operational Notes

The API loads approved model artifacts from MLflow using `MODEL_RUN_ID`.

The approved artifact path is `approved_model`.

The model artifact is verified with SHA256 before serving predictions.

The API logs structured prediction and recommendation events.

Each prediction and recommendation response includes a unique `request_id`.

The local API key is for development only. Production should use a managed secret store and stronger authentication.

The current model is a MovieLens matrix factorization recommender trained on the MovieLens latest small dataset.