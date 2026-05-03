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

### Request Rules

| Field | Type | Rule |
|---|---|---|
| user_id | integer | Must exist in the approved MovieLens user mapping |
| top_n | integer | Optional. Defaults to 10. Must be between 1 and 50 |

### Success Response

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

### Recommendation Item Fields

| Field | Type | Description |
|---|---|---|
| movie_id | integer | Recommended MovieLens movie ID |
| title | string | Movie title from `movies_metadata.csv` |
| genres | string | Pipe separated MovieLens genres |
| predicted_rating | float | Predicted rating for the recommended movie |
| GET | /movies/{movie_id} | Returns title and genre metadata for one movie |

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

| Error Code | Status | Applies To |
|---|---:|---|
| AUTH_INVALID_API_KEY | 401 | `/predict`, `/recommend` |
| UNKNOWN_USER_ID | 404 | `/predict`, `/recommend` |
| UNKNOWN_MOVIE_ID | 404 | `/predict`, `/movies/{movie_id}` |
| RATE_LIMIT_EXCEEDED | 429 | `/predict`, `/recommend` |
| PREDICTION_FAILED | 500 | `/predict` |
| RECOMMENDATION_FAILED | 500 | `/recommend` |

### Error Responses

| Condition | Status |
|---|---|
| Missing API key | 401 |
| Invalid API key | 401 |
| Missing `user_id` | 422 |
| Invalid `top_n` | 422 |
| Unknown `user_id` | 404 |