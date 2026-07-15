# Three Month Feature Improvement Plan for Lumina Rec

## Goal

Move Lumina Rec from a strong local MLOps portfolio project into a more complete, production shaped recommendation platform.

## Target Outcome

After three months, Lumina Rec should support:

- Approved model serving through MLflow Model Registry
- Dataset validation
- Artifact validation
- Stronger API coverage
- Recommendation quality metrics
- Richer observability
- Clearer production deployment path

## Month 1, Strengthen the Core Platform

Theme: Make the current application stable, testable, and governed.

### Week 1, Dataset Validation and Training Gates

Objective: Prevent bad training runs from entering MLflow.

Build:

- Wire `src/lumina_rec/validation/dataset_checks.py` into the project runner
- Add `.\scripts\lumina.ps1 validate-data`
- Validate `ratings.csv` and `movies.csv`
- Validate required columns
- Validate ratings are between 0.5 and 5.0
- Validate movie IDs in ratings exist in `movies.csv`
- Add dataset validation tests
- Generate a simple dataset validation report

Files:

- `src/lumina_rec/validation/dataset_checks.py`
- `scripts/lumina.ps1`
- `tests/unit/validation/test_dataset_checks.py`
- `reports/dataset_validation_report.md`
- `docs/dataset_validation_plan.md`

Acceptance criteria:

- `.\scripts\lumina.ps1 validate-data` passes
- Dataset validation tests pass
- Training does not proceed if required dataset checks fail

### Week 2, Artifact Manifest Validation

Objective: Confirm the model, mappings, metadata, and movie metadata belong to the same approved package.

Build:

- Generate `artifact_manifest.json` during training
- Include MLflow run ID, model name, model version, model SHA256, mappings SHA256, movie metadata SHA256, and created timestamp
- Load and validate the manifest during inference startup
- Fail startup if the manifest is missing or mismatched
- Add tests for manifest validation logic

Files:

- `ml/training/train.py`
- `services/inference/main.py`
- `src/lumina_rec/validation/artifact_manifest.py`
- `tests/unit/validation/test_artifact_manifest.py`
- `docs/artifact_manifest_plan.md`

Acceptance criteria:

- Inference fails safely when artifact files do not match the manifest
- `/ready` shows artifact manifest validation status
- Tests cover valid and invalid manifest cases

### Week 3, MLflow Model Registry Alias

Objective: Remove hard dependency on manually setting `MODEL_RUN_ID`.

Build:

- Complete `src/lumina_rec/registry/register_model.py`
- Register approved model as `lumina-rec-movielens-mf`
- Assign alias `approved`
- Add inference support for `USE_MODEL_REGISTRY=true`
- Keep current `MODEL_RUN_ID` path as fallback
- Add registry validation script

Files:

- `src/lumina_rec/registry/register_model.py`
- `src/lumina_rec/registry/resolve_model.py`
- `services/inference/main.py`
- `scripts/lumina.ps1`
- `.env.example`
- `docs/model_registry_plan.md`

Acceptance criteria:

- Inference starts with `MODEL_RUN_ID`
- Inference starts with `USE_MODEL_REGISTRY=true`
- `/ready` shows model registry alias and resolved run ID

### Week 4, API Contract Hardening

Objective: Make the API easier to use, test, and extend.

Build:

- Add structured error response model
- Add `/version` endpoint
- Add `/model` endpoint for current serving model metadata
- Add clear error codes for missing API key, invalid API key, unknown user, unknown movie, invalid `top_n`, and model unavailable
- Update tests and API docs

Acceptance criteria:

- API returns predictable error responses
- Tests cover new endpoints and error paths
- Docs match actual API behavior

## Month 2, Improve Recommendation Quality and Usability

Theme: Make the recommender more useful and measurable.

### Week 5, Recommendation Quality Metrics

Objective: Stop relying only on RMSE.

Build:

- Add ranking evaluation module
- Calculate Precision at K, Recall at K, NDCG at K, and Coverage
- Store metrics in MLflow
- Add a model quality report
- Update model promotion gate

Files:

- `src/lumina_rec/evaluation/ranking_metrics.py`
- `src/lumina_rec/evaluation/evaluate_recommender.py`
- `tests/unit/evaluation/test_ranking_metrics.py`
- `reports/templates/recommendation_quality_report.md`

Acceptance criteria:

- Training logs ranking metrics to MLflow
- Promotion checklist includes ranking metrics
- Candidate model promotion does not depend on RMSE alone

### Week 6, Better Recommendation Endpoint

Objective: Make `/recommend` more useful for demos and reviews.

Build:

- Add optional genre filter
- Add optional minimum rating threshold
- Add optional exclude previously rated flag
- Add rank to each recommendation item
- Add response count metadata

Example request:

```json
{
  "user_id": 1,
  "top_n": 10,
  "genre": "Comedy",
  "min_rating": 4.0,
  "exclude_seen": true
}