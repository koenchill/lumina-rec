# Model Promotion Record

## Purpose

This file records the approved model promotion decision for Lumina Rec.

## Approved Model

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

## Promotion Reason

This model is promoted because it completed training, logged artifacts to MLflow, and produced a better RMSE than the previous approved model.

## Previous Approved Model

| Field | Value |
|---|---|
| MLflow run ID | 248c55bf41994c05923a86e354158303 |
| Model SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 |
| Test RMSE | 2.0423 |

## Decision

Approved for local inference validation.

## Required Runtime Values

```env
MODEL_RUN_ID=14eda4cf03bd4d328a3ee791ec9a002f
MODEL_SHA256=205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd
MODEL_ARTIFACT_PATH=approved_model