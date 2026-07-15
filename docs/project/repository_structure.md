# Repository Structure

## Purpose

This file explains the main folders and files in Lumina Rec after the staged layout reorg.

## Structure

```text
lumina-rec/
├── .github/
│   └── workflows/
│       └── ci.yml
├── configs/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── architecture/
│   ├── api/
│   │   └── examples/
│   ├── mlops/
│   ├── operations/
│   ├── security/
│   ├── plans/
│   └── project/
├── feature-store/
├── infra/
│   └── terraform/
├── ml/
│   ├── models/                 # generated local artifacts (gitignored)
│   └── training/
│       └── train.py            # training job entrypoint
├── notebooks/
├── reports/
│   └── templates/
├── scripts/
├── services/
│   └── inference/
│       ├── app/                # FastAPI application package
│       ├── Dockerfile
│       └── requirements.txt
├── src/
│   └── lumina_rec/             # shared Python library
│       ├── models/
│       ├── evaluation/
│       ├── registry/
│       └── validation/
├── tests/
│   ├── inference/
│   ├── load/
│   └── unit/
│       ├── evaluation/
│       └── validation/
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── uv.lock
```

## Key Runtime Files

| File | Purpose |
|---|---|
| `src/lumina_rec/` | Shared model, evaluation, registry, and validation code |
| `ml/training/train.py` | Trains the MovieLens recommender and logs approved artifacts to MLflow |
| `services/inference/app/main.py` | FastAPI inference application |
| `services/inference/Dockerfile` | Builds the inference container |
| `scripts/lumina.ps1` | Windows task runner |
| `docker-compose.yml` | Local service orchestration |
| `tests/inference/test_api.py` | API tests |
| `tests/unit/` | Unit tests for shared library code |
| `tests/load/locustfile.py` | Load test |

## Documentation Layout

| Folder | Purpose |
|---|---|
| `docs/architecture/` | System design, data flow, ADRs |
| `docs/api/` | API contract, examples, OpenAPI notes |
| `docs/mlops/` | Model card, promotion, rollback, testing |
| `docs/operations/` | Setup, runbooks, env vars, commands |
| `docs/security/` | Threat model, controls, access |
| `docs/plans/` | Future work (not current product truth) |
| `docs/project/` | Status, handoff, roadmap, review guides |

## Generated Files Not Committed

| Path | Reason |
|---|---|
| `.env` | Local secrets and runtime values |
| `.venv/` | Local Python environment |
| `__pycache__/` | Python bytecode cache |
| `ml/models/*` (except README) | Training output and download cache |
| `tests/load/load_test_report.html` | Generated load test report |
| `.pytest_cache/` | Pytest cache |

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |
