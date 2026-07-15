# Tests

## Purpose

Validation tests for Lumina Rec.

## Layout

| Folder | Purpose |
|---|---|
| `tests/unit/` | Shared library tests (evaluation, validation, registry) |
| `tests/inference/` | FastAPI endpoint tests |
| `tests/load/` | Locust load tests |

## Run Tests

```powershell
.\scripts\lumina.ps1 test
```

Or directly:

```powershell
pytest tests/unit -q
pytest tests/inference/test_api.py
```

Inference API tests require the approved model to load (local MLflow stack or cached artifacts under `ml/models/approved/`).
