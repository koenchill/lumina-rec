# Lumina Rec Model Card

## Model Summary

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Version | 0.2.0 |
| Model type | Matrix factorization |
| Framework | PyTorch |
| Dataset | MovieLens latest small |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

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