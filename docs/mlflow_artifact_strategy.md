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

## Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 248c55bf41994c05923a86e354158303 |
| Artifact path | approved_model |
| Model SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 |

## Approved Artifacts

| Artifact | Purpose |
|---|---|
| recommender_model.pt | PyTorch model payload |
| model_metadata.json | Model metadata, metrics, checksum, run ID |
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
7. Serve predictions.

## Acceptance Rules

A model is considered approved when:

- Training completes.
- Test metrics are logged.
- Required artifacts are present.
- SHA256 is recorded.
- Inference starts successfully.
- `/ready` confirms the run ID and checksum.
- `/predict` returns a valid response.