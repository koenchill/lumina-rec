# Release Notes

## Current Release

Version: 0.2.0

## Summary

Lumina Rec moved from a demo linear model to a MovieLens matrix factorization recommender.

## Added

- MovieLens training workflow
- MLflow approved artifact loading
- SHA256 model checksum validation
- `/predict` rating prediction endpoint
- `/recommend` top N recommendation endpoint
- Recommendation API documentation
- Model card
- Promotion record
- Rollback procedure
- Threat model updates
- Security controls updates
- Operational runbooks

## Changed

- Inference now loads approved MLflow artifacts instead of a local demo model.
- API payload changed from feature vector input to MovieLens IDs.
- Approved model selection now uses `MODEL_RUN_ID` and `MODEL_SHA256`.

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Known Limitations

- Recommendation responses do not include movie title or genres yet.
- Model Registry alias is not implemented yet.
- Dataset checksum validation is not implemented yet.
- Production deployment is not implemented yet.