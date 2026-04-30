# Lumina Rec Model Card

## Model Summary

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Version | 0.2.0 |
| Model type | Matrix factorization |
| Framework | PyTorch |
| Dataset | MovieLens latest small |
| MLflow run ID | 248c55bf41994c05923a86e354158303 |
| Artifact path | approved_model |
| SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 |

## Intended Use

This model predicts a user’s rating for a movie and supports top N recommendation workflows.

## Not Intended For

This model is not intended for production personalization, regulated decision making, or user profiling.

## Training Data

The model uses the MovieLens latest small dataset.

The dataset includes user ratings for movies. It is used here for local MLOps demonstration and recommender system practice.

## Model Inputs

| Input | Type | Description |
|---|---|---|
| user_id | integer | MovieLens user ID |
| movie_id | integer | MovieLens movie ID |

## Model Output

| Output | Type | Description |
|---|---|---|
| predicted_rating | float | Predicted rating from 0.5 to 5.0 |

## Performance

| Metric | Value |
|---|---|
| Test RMSE | 2.0423 |

## Limitations

- Baseline model only.
- No hyperparameter tuning yet.
- No cold start handling yet.
- No movie title metadata in recommendation responses yet.
- No fairness or bias analysis yet.
- No production monitoring yet.

## Governance

The model is approved by MLflow run ID and verified by SHA256 before inference startup.