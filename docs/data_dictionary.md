# Data Dictionary

## Purpose

This document defines the dataset fields, derived fields, and model artifacts used by Lumina Rec.

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
| user_idx | integer | Encoded user index used by the PyTorch embedding layer |
| movie_idx | integer | Encoded movie index used by the PyTorch embedding layer |

## Model Input Fields

## `/predict`

| Field | Type | Rule |
|---|---|---|
| user_id | integer | Must exist in `movielens_mappings.json` |
| movie_id | integer | Must exist in `movielens_mappings.json` |

## `/recommend`

| Field | Type | Rule |
|---|---|---|
| user_id | integer | Must exist in `movielens_mappings.json` |
| top_n | integer | Must be between 1 and 50 |

## Model Output Fields

## `/predict`

| Field | Type | Description |
|---|---|---|
| predicted_rating | float | Predicted rating from 0.5 to 5.0 |
| user_id | integer | Requested user ID |
| movie_id | integer | Requested movie ID |
| model_name | string | Approved model name |
| model_version | string | Approved model version |
| request_id | string | Unique request identifier |
| latency_ms | float | Request processing time in milliseconds |

## `/recommend`

| Field | Type | Description |
|---|---|---|
| user_id | integer | Requested user ID |
| recommendations | list | Ranked list of recommended movies |
| movie_id | integer | Recommended MovieLens movie ID |
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
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |