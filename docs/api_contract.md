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
```

````markdown
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

### Success Response

```json
{
  "user_id": 1,
  "recommendations": [
    {
      "movie_id": 2,
      "title": "Jumanji (1995)",
      "genres": "Adventure|Children|Fantasy",
      "predicted_rating": 5.0
    },
    {
      "movie_id": 3,
      "title": "Grumpier Old Men (1995)",
      "genres": "Comedy|Romance",
      "predicted_rating": 5.0
    }
  ],
  "model_name": "lumina-rec-movielens-mf",
  "model_version": "0.2.0",
  "request_id": "example-request-id",
  "latency_ms": 3.83
}
```

### Recommendation Item Fields

| Field | Type | Description |
|---|---|---|
| movie_id | integer | Recommended MovieLens movie ID |
| title | string | Movie title from `movies_metadata.csv` |
| genres | string | Pipe separated MovieLens genres |
| predicted_rating | float | Predicted rating for the recommended movie |

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

FastAPI schema validation errors still return the default 422 response.

### Error Responses

| Condition | Status |
|---|---|
| Missing API key | 401 |
| Invalid API key | 401 |
| Missing `user_id` | 422 |
| Invalid `top_n` | 422 |
| Unknown `user_id` | 404 |
| GET | /movies/{movie_id} | No | Returns movie title and genre metadata |
| GET | /version | No | Returns service and model version metadata |
| GET | /model | No | Returns current approved model serving metadata |

