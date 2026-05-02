# Tests

## Purpose

This folder stores validation tests for Lumina Rec.

## Test Areas

| Folder | Purpose |
|---|---|
| tests/inference | FastAPI endpoint tests |
| tests/load | Locust load tests |

## Current API Test Coverage

The API tests validate:

- `/health`
- `/ready`
- `/movies/{movie_id}`
- `/predict`
- `/recommend`
- `/metrics`
- authentication failures
- validation failures
- unknown user handling
- unknown movie handling

## Run Tests

```powershell
.\scripts\lumina.ps1 test