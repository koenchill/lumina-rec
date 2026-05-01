# Data Dictionary

## Purpose

This document defines the dataset fields, derived fields, API request fields, API response fields, and model artifacts used by Lumina Rec.

## Dataset

MovieLens latest small.

## Source Files

| File | Purpose |
|---|---|
| ratings.csv | User movie ratings |
| movies.csv | Movie metadata |

## ratings.csv

| Column | Type | Description |
|---|---|---|
| userId | integer | User identifier from MovieLens |
| movieId | integer | Movie identifier from MovieLens |
| rating | float | User rating for a movie |
| timestamp | integer | Rating event timestamp |

## movies.csv

| Column | Type | Description |
|---|---|---|
| movieId | integer | Movie identifier from MovieLens |
| title | string | Movie title |
| genres | string | Pipe separated movie genres |

## Derived Training Fields

| Field | Type | Description |
|---|---|---|
| user_idx | integer | Encoded user index used by the PyTorch user embedding layer |
| movie_idx | integer | Encoded movie index used by the PyTorch movie embedding layer |

## API Request Fields

### POST /predict

| Field | Type | Rule |
|---|---|---|
| user_id | integer | Must exist in `movielens_mappings.json` |
| movie_id | integer | Must exist in `movielens_mappings.json` |

### POST /recommend

| Field | Type | Rule |
|---|---|---|
| user_id | integer | Must exist in `movielens_mappings.json` |
| top_n | integer | Optional. Defaults to 10. Must be between 1 and 50 |

## API Response Fields

### POST /predict

| Field | Type | Description |
|---|---|---|
| predicted_rating | float | Predicted rating from 0.5 to 5.0 |
| user_id | integer | Requested user ID |
| movie_id | integer | Requested movie ID |
| model_name | string | Approved model name |
| model_version | string | Approved model version |
| request_id | string | Unique request identifier |
| latency_ms | float | Request processing time in milliseconds |

### POST /recommend

| Field | Type | Description |
|---|---|---|
| user_id | integer | Requested user ID |
| recommendations | list | Ranked list of recommended movies |
| movie_id | integer | Recommended MovieLens movie ID |
| title | string | Movie title from `movies_metadata.csv` |
| genres | string | Pipe separated MovieLens genres |
| predicted_rating | float | Predicted rating for the recommended movie |
| model_name | string | Approved model name |
| model_version | string | Approved model version |
| request_id | string | Unique request identifier |
| latency_ms | float | Request processing time in milliseconds |

## Model Artifacts

| Artifact | Purpose |
|---|---|
| recommender_model.pt | PyTorch model payload |
| model_metadata.json | Model metadata, metrics, checksum, and run ID |
| movielens_mappings.json | User and movie ID mappings |
| movies_metadata.csv | Movie title and genre metadata |

## Current Approved Model Metadata

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| Dataset | MovieLens latest small |
| Model type | Matrix factorization |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Validation Notes

The `/recommend` response now includes movie metadata.

Expected recommendation item fields:

```json
{
  "movie_id": 2,
  "title": "Jumanji (1995)",
  "genres": "Adventure|Children|Fantasy",
  "predicted_rating": 5.0
}
```

## Known Limitations

- Movie metadata is loaded from the approved MLflow artifact package.
- Missing metadata falls back to `Unknown title` and `Unknown`.
- No `/movies/{movie_id}` lookup endpoint exists yet.
- No genre filter exists yet.