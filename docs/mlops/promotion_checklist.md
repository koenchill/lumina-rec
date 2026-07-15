# Model Promotion Checklist

## Purpose

This checklist defines the minimum checks before approving a new model for inference.

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Dataset | MovieLens latest small |
| Test RMSE | 2.0162 |

## Candidate Model Information

| Field | Value |
|---|---|
| Model name |  |
| Model version |  |
| MLflow run ID |  |
| Artifact path | approved_model |
| Model SHA256 |  |
| Dataset |  |
| Test RMSE |  |

## Required Artifacts

| Artifact | Required | Present |
|---|---|---|
| recommender_model.pt | Yes |  |
| model_metadata.json | Yes |  |
| movielens_mappings.json | Yes |  |
| movies_metadata.csv | Yes |  |

## Required Checks

| Check | Required Result | Pass |
|---|---|---|
| Training completed | Yes |  |
| MLflow run logged | Yes |  |
| Test RMSE recorded | Yes |  |
| Model SHA256 recorded | Yes |  |
| Required artifacts present | Yes |  |
| MinIO `mlflow-artifacts` bucket exists | Yes |  |
| Docker inference starts | Yes |  |
| `/health` passes | Yes |  |
| `/ready` passes | Yes |  |
| `/predict` passes | Yes |  |
| `/recommend` passes | Yes |  |
| API tests pass | Yes |  |
| Load test has 0 failures | Yes |  |
| New RMSE is equal or better than approved baseline | Preferred |  |

## Promotion Steps

1. Train the candidate model.

```powershell
.\scripts\lumina.ps1 train
```

2. Record the candidate values.

```text
Run ID
Model SHA256
Test RMSE
```

3. Compare the candidate RMSE to the approved baseline.

4. Update `.env` only if the candidate is approved.

```env
MODEL_RUN_ID=<candidate_run_id>
MODEL_SHA256=<candidate_model_sha256>
MODEL_ARTIFACT_PATH=approved_model
```

5. Restart inference.

```powershell
docker compose stop inference
docker compose rm -f inference
docker compose up -d --build inference
```

6. Validate the promoted model.

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 load-test
```

## Approval Decision

| Decision | Notes |
|---|---|
| Approved |  |
| Rejected |  |
| Needs retraining |  |

## Rollback Reference

Keep the previous approved `MODEL_RUN_ID` and `MODEL_SHA256` before promoting a new model.

Current rollback candidate:

| Field | Value |
|---|---|
| Previous MLflow run ID | 248c55bf41994c05923a86e354158303 |
| Previous model SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 |
| Previous test RMSE | 2.0423 |