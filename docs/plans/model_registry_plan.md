# Model Registry Plan

## Purpose

This document defines the future model registry plan for Lumina Rec.

## Current State

The current approved model is selected with environment variables.

| Variable | Purpose |
|---|---|
| MODEL_RUN_ID | Selects the approved MLflow run |
| MODEL_ARTIFACT_PATH | Selects artifact folder |
| MODEL_SHA256 | Verifies model integrity |

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Target State

Use MLflow Model Registry to manage model promotion.

## Proposed Stages

| Stage | Meaning |
|---|---|
| candidate | Model trained and logged |
| staging | Model passed local validation |
| approved | Model approved for serving |
| archived | Model retired or replaced |

## Promotion Criteria

A model should move to approved only after:

- Training completes
- Required artifacts exist
- RMSE is recorded
- SHA256 is recorded
- `/ready` passes
- `/predict` passes
- `/recommend` passes
- API tests pass
- Load test passes with 0 failures

## Future Work

- Add model registry registration
- Add approved alias
- Load by alias instead of hard coded run ID
- Add promotion automation
- Add rollback automation