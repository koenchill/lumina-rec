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
| GET | /movies/{movie_id} | Returns title and genre metadata for one movie |

### Error Responses

| Condition | Status |
|---|---|
| Missing API key | 401 |
| Invalid API key | 401 |
| Missing `user_id` | 422 |
| Invalid `top_n` | 422 |
| Unknown `user_id` | 404 |