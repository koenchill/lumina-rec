# Data Dictionary

## Dataset

MovieLens latest small.

## ratings.csv

| Column | Type | Description |
|---|---|---|
| userId | integer | User identifier |
| movieId | integer | Movie identifier |
| rating | float | User rating for a movie |
| timestamp | integer | Rating event timestamp |

## movies.csv

| Column | Type | Description |
|---|---|---|
| movieId | integer | Movie identifier |
| title | string | Movie title |
| genres | string | Pipe separated movie genres |

## Derived Fields

| Field | Type | Description |
|---|---|---|
| user_idx | integer | Encoded user index used by the model |
| movie_idx | integer | Encoded movie index used by the model |

## Model Artifacts

| Artifact | Purpose |
|---|---|
| recommender_model.pt | PyTorch model payload |
| model_metadata.json | Model metadata, run ID, checksum, metrics |
| movielens_mappings.json | User and movie ID mappings |
| movies_metadata.csv | Movie title and genre metadata |