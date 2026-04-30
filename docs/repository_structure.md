# Repository Structure

## Purpose

This file explains the main folders and files in Lumina Rec.

## Structure

```text
lumina-rec/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── api_contract.md
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── docker_cleanup.md
│   ├── environment_variables.md
│   ├── incident_response_runbook.md
│   ├── local_validation.md
│   ├── mlflow_artifact_strategy.md
│   ├── model_card.md
│   ├── model_promotion_record.md
│   ├── model_rollback_procedure.md
│   ├── operational_commands.md
│   ├── project_status.md
│   ├── promotion_checklist.md
│   ├── recommendation_api.md
│   ├── repository_structure.md
│   ├── reviewer_guide.md
│   ├── runbook_quickstart.md
│   ├── security_controls.md
│   ├── testing_strategy.md
│   └── threat_model.md
├── feature-store/
├── ml/
│   ├── models/
│   └── training/
│       └── train.py
├── scripts/
│   └── lumina.ps1
├── services/
│   └── inference/
│       ├── Dockerfile
│       ├── main.py
│       └── requirements.txt
├── tests/
│   ├── inference/
│   │   └── test_api.py
│   └── load/
│       └── locustfile.py
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── uv.lock
```

## Key Runtime Files

| File | Purpose |
|---|---|
| ml/training/train.py | Trains the MovieLens recommender and logs approved artifacts to MLflow |
| services/inference/main.py | FastAPI inference service for `/predict` and `/recommend` |
| services/inference/Dockerfile | Builds the inference container |
| services/inference/requirements.txt | Pins inference container dependencies |
| scripts/lumina.ps1 | Windows task runner |
| docker-compose.yml | Local service orchestration |
| tests/inference/test_api.py | API tests |
| tests/load/locustfile.py | Load test |

## Key Documentation Files

| File | Purpose |
|---|---|
| docs/api_contract.md | Defines API endpoints, payloads, and responses |
| docs/architecture.md | Explains architecture and service flow |
| docs/model_card.md | Documents the approved MovieLens model |
| docs/model_promotion_record.md | Records the current approved model decision |
| docs/mlflow_artifact_strategy.md | Explains approved artifact loading from MLflow |
| docs/recommendation_api.md | Documents `/predict` and `/recommend` |
| docs/security_controls.md | Maps controls to risk reduction |
| docs/threat_model.md | Documents threats and planned mitigations |
| docs/testing_strategy.md | Explains API and load test coverage |
| docs/runbook_quickstart.md | Provides quick local validation steps |
| docs/operational_commands.md | Lists common commands |

## Generated Files Not Committed

| Path | Reason |
|---|---|
| .env | Local secrets and runtime values |
| .venv/ | Local Python environment |
| __pycache__/ | Python bytecode cache |
| ml/models/approved/ | Downloaded MLflow artifact cache |
| ml/models/*.pt | Generated model files |
| tests/load/load_test_report.html | Generated load test report |
| .pytest_cache/ | Pytest cache |

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |