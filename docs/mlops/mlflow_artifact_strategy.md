# MLflow Artifact Strategy

## Purpose

This document explains how Lumina Rec uses MLflow to track, approve, and serve model artifacts.

## Current Strategy

Lumina Rec trains a MovieLens matrix factorization recommender and logs the approved artifacts to MLflow.

The inference API loads the approved model using:

| Variable | Purpose |
|---|---|
| MODEL_RUN_ID | MLflow run that contains the approved artifacts |
| MODEL_ARTIFACT_PATH | Artifact folder inside the run |
| MODEL_SHA256 | Approved checksum for the model artifact |
| MLFLOW_TRACKING_URI | MLflow tracking server URL |
| MLFLOW_S3_ENDPOINT_URL | MinIO S3 compatible endpoint |

## Current Approved Model

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

## Approved Artifacts

| Artifact | Purpose |
|---|---|
| recommender_model.pt | PyTorch model payload |
| model_metadata.json | Model metadata, metrics, checksum, and run ID |
| movielens_mappings.json | User and movie index mappings |
| movies_metadata.csv | Movie title and genre metadata |

## Training Flow

1. Download MovieLens latest small dataset.
2. Train the PyTorch matrix factorization model.
3. Evaluate test RMSE.
4. Save model payload.
5. Calculate SHA256.
6. Write metadata file.
7. Log artifacts to MLflow under `approved_model`.

## Inference Flow

1. Read `MODEL_RUN_ID`.
2. Connect to MLflow.
3. Download artifacts from `approved_model`.
4. Verify the model checksum.
5. Load mappings.
6. Load the PyTorch model.
7. Serve `/predict` and `/recommend`.

## Promotion Flow

1. Train a candidate model.
2. Compare candidate RMSE against the approved baseline.
3. Confirm artifacts uploaded to MLflow.
4. Confirm SHA256 was recorded.
5. Update `.env` with the approved `MODEL_RUN_ID` and `MODEL_SHA256`.
6. Restart inference.
7. Validate `/ready`, `/predict`, `/recommend`, and tests.
8. Record the decision in `docs/model_promotion_record.md`.

## Current Promotion Decision

The current approved model replaced the previous run because its RMSE improved from `2.0423` to `2.0162`.

| Metric | Previous | Current | Result |
|---|---:|---:|---|
| Test RMSE | 2.0423 | 2.0162 | Improved |

## Runtime Validation

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test
```

## Acceptance Rules

A model is considered approved when:

- Training completes.
- Test metrics are logged.
- Required artifacts are present.
- SHA256 is recorded.
- Inference starts successfully.
- `/ready` confirms the run ID and checksum.
- `/predict` returns a valid response.
- `/recommend` returns a valid recommendation list.
- API tests pass.

## Future Improvements

- Add MLflow Model Registry alias for approved model.
- Add signed artifact verification.
- Add dataset checksum validation.
- Add model performance gate before promotion.
- Add automated promotion report generation.