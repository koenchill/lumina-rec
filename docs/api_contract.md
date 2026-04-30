# Lumina Rec Inference API Contract

## Base URL

Local:

```text
http://localhost:8001
```

## Authentication

The `/predict` endpoint requires an API key.

Required header:

```http
x-api-key: local-dev-api-key
```

Health, readiness, and metrics endpoints do not require an API key in the local development setup.

## Endpoints

| Method | Endpoint | Authentication | Purpose |
|---|---|---|---|
| GET | /health | No | Confirms the API process is running |
| GET | /ready | No | Confirms the approved model artifact is loaded |
| GET | /metrics | No | Exposes Prometheus style metrics |
| POST | /predict | Yes | Returns a MovieLens rating prediction |

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
  "model_run_id": "248c55bf41994c05923a86e354158303",
  "model_artifact_path": "approved_model",
  "model_sha256": "c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6",
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
  "latency_ms": 9.25
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

If `user_id` or `movie_id` is missing, the API returns:

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

The API logs structured prediction events.

Each prediction response includes a unique `request_id`.

The local API key is for development only. Production should use a managed secret store and stronger authentication.

The current model is a MovieLens matrix factorization recommender trained on the MovieLens latest small dataset.