# Model Risk Management

## Purpose

This document identifies model risks and controls for Lumina Rec.

## Model Risks

| Risk | Impact | Current Control |
|---|---|---|
| Wrong model served | Bad predictions | MODEL_RUN_ID and SHA256 validation |
| Model artifact tampering | Integrity loss | SHA256 checksum |
| Weak model quality | Poor recommendations | RMSE tracking |
| Dataset issue | Poor training output | Planned dataset validation |
| Mismatched mappings | Runtime errors | Artifacts logged together |
| Cold start users | Unsupported requests | Unknown user returns 404 |
| Cold start movies | Unsupported requests | Unknown movie returns 404 |

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Future Controls

- Add ranking metrics.
- Add dataset checksum validation.
- Add artifact manifest validation.
- Add MLflow Model Registry alias.
- Add model rollback automation.