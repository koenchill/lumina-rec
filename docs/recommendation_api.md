# Recommendation API

## Purpose

The recommendation API returns MovieLens rating predictions and top N movie recommendations for a known user.

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

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /predict | Predicts a rating for one user and one movie |
| POST | /recommend | Returns top N recommendations for one user |

## Authentication

Both endpoints require:

```text
x-api-key: local-dev-api-key
```

## POST /predict

### Request

```json
{
  "user_id": 1,
  "movie_id": 1
}
```

### Response

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

```json
{
  "user_id": 1,
  "top_n": 10
}
```

### Response

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

## Validation Rules

| Field | Rule |
|---|---|
| user_id | Must exist in the approved MovieLens mappings |
| movie_id | Must exist in the approved MovieLens mappings |
| top_n | Must be between 1 and 50 |

## Error Responses

| Condition | Status |
|---|---|
| Missing API key | 401 |
| Invalid API key | 401 |
| Missing required field | 422 |
| Invalid `top_n` | 422 |
| Unknown user_id | 404 |
| Unknown movie_id | 404 |