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
| Artifact path | approved_model |
| SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Intended Use

This model supports local recommendation system development and MLOps practice.

It provides:

- Rating prediction for one user and one movie through `/predict`
- Top N recommendations for one user through `/recommend`

## Not Intended For

This model is not intended for:

- Production personalization
- Regulated decision making
- User profiling
- Financial, healthcare, legal, employment, or eligibility decisions
- Real customer recommendation systems without additional validation

## Training Data

The model uses the MovieLens latest small dataset.

The dataset contains user ratings for movies. It is used here for local MLOps demonstration and recommender system practice.

## Model Inputs

### Prediction Input

| Input | Type | Description |
|---|---|---|
| user_id | integer | MovieLens user ID |
| movie_id | integer | MovieLens movie ID |

### Recommendation Input

| Input | Type | Description |
|---|---|---|
| user_id | integer | MovieLens user ID |
| top_n | integer | Number of recommendations requested, between 1 and 50 |

## Model Outputs

### Prediction Output

| Output | Type | Description |
|---|---|---|
| predicted_rating | float | Predicted rating from 0.5 to 5.0 |
| user_id | integer | Input user ID |
| movie_id | integer | Input movie ID |
| request_id | string | Unique request identifier |
| latency_ms | float | API processing latency |

### Recommendation Output

| Output | Type | Description |
|---|---|---|
| recommendations | list | Ranked list of recommended movie IDs and predicted ratings |
| movie_id | integer | Recommended MovieLens movie ID |
| predicted_rating | float | Predicted rating for the recommended movie |
| request_id | string | Unique request identifier |
| latency_ms | float | API processing latency |

## Performance

| Metric | Value |
|---|---|
| Test RMSE | 2.0162 |

The current approved model improved over the previous approved baseline.

| Metric | Previous | Current |
|---|---:|---:|
| Test RMSE | 2.0423 | 2.0162 |

## Validation

The approved model passed:

- Training completion
- MLflow artifact logging
- SHA256 checksum generation
- Inference startup
- `/ready` validation
- `/predict` validation
- `/recommend` validation
- API tests
- Load test with zero failures

## Limitations

- Baseline model only
- No hyperparameter tuning yet
- No cold start handling yet
- No movie title metadata in recommendation responses yet
- No fairness or bias analysis yet
- No production monitoring yet
- No MLflow Model Registry alias yet
- No dataset checksum validation yet

## Governance

The model is approved by MLflow run ID and verified by SHA256 before inference startup.

Current approved runtime values:

```env
MODEL_RUN_ID=14eda4cf03bd4d328a3ee791ec9a002f
MODEL_SHA256=205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd
MODEL_ARTIFACT_PATH=approved_model
```

## Recommended Next Improvements

- Add movie title and genre metadata to recommendation responses
- Add `/movies/{movie_id}` endpoint
- Add MLflow Model Registry alias for approved model selection
- Add dataset checksum validation
- Add recommendation quality metrics
- Add model performance gate before promotion