# Artifact Manifest Plan

## Purpose

This document defines the plan for validating that approved MLflow artifacts belong together.

## Current Approved Artifacts

| Artifact | Purpose |
|---|---|
| recommender_model.pt | PyTorch model payload |
| model_metadata.json | Model metadata and metrics |
| movielens_mappings.json | User and movie index mappings |
| movies_metadata.csv | Movie metadata |

## Current Risk

The inference service expects these artifacts to match the same model run.

If artifacts are missing or mismatched, predictions and recommendations can break.

## Target Manifest

Add an `artifact_manifest.json` file with:

| Field | Purpose |
|---|---|
| run_id | MLflow run ID |
| model_name | Approved model name |
| model_version | Approved model version |
| model_sha256 | Model checksum |
| mappings_sha256 | Mappings checksum |
| movies_metadata_sha256 | Movie metadata checksum |
| created_at | Manifest creation timestamp |

## Future Validation

Inference should validate:

- Required artifacts exist
- Model checksum matches
- Mappings checksum matches
- Metadata checksum matches
- Manifest run ID matches `MODEL_RUN_ID`

## Benefit

Artifact manifest validation reduces risk from partial uploads, stale mappings, and mismatched artifacts.