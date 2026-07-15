# Local Model Artifacts

This directory holds **generated** training outputs and the local MLflow download cache.

## Contents

| Path | Purpose | Committed? |
|---|---|---|
| `approved/` | Inference download cache from MLflow | No |
| `*.pt` / `*.pth` | Model weight files | No |
| `movielens_mappings.json` | Training ID mappings | No |
| `movies_metadata.csv` | Movie title/genre table written by training | No |
| `model_metadata.json` | Training metadata written by training | No |
| `artifact_manifest.json` | Artifact integrity manifest | No |
| `latest_run.json` | Convenience pointer to latest local run | No |

Source of truth for approved serving artifacts is **MLflow** (MinIO), not this folder.

Training writes here before `mlflow.log_artifacts`. Inference downloads into `approved/`.
