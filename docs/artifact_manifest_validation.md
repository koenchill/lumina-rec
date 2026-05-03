# Artifact Manifest Validation

## Purpose

Artifact manifest validation confirms that approved model artifacts belong together and have not changed unexpectedly.

## Current Required Artifacts

| Artifact | Purpose |
|---|---|
| recommender_model.pt | PyTorch model payload |
| model_metadata.json | Model metadata and metrics |
| movielens_mappings.json | User and movie mappings |
| movies_metadata.csv | Movie title and genre metadata |

## Manifest File

Planned manifest file:

```text
artifact_manifest.json