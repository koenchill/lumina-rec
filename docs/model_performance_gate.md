# Model Performance Gate

## Purpose

This document defines the minimum model performance checks before promotion.

## Current Approved Baseline

| Metric | Value |
|---|---|
| Test RMSE | 2.0162 |

## Current Promotion Rule

A candidate model should not replace the approved model unless it has an equal or better RMSE, or there is a clear technical reason to promote it.

## Required Candidate Checks

| Check | Required |
|---|---|
| Training completes | Yes |
| MLflow run created | Yes |
| Approved artifacts uploaded | Yes |
| Test RMSE recorded | Yes |
| Model SHA256 recorded | Yes |
| `/ready` passes | Yes |
| `/predict` passes | Yes |
| `/recommend` passes | Yes |
| API tests pass | Yes |
| Load test has 0 failures | Yes |

## Future Ranking Metrics

RMSE alone is not enough for recommendation quality.

Future gates should include:

| Metric | Purpose |
|---|---|
| Precision at K | Measures useful top K recommendations |
| Recall at K | Measures relevant item coverage |
| NDCG at K | Measures ranking quality |
| Coverage | Measures catalog spread |
| Diversity | Measures recommendation variety |

## Decision Outcomes

| Outcome | Meaning |
|---|---|
| Approved | Candidate replaces current model |
| Rejected | Candidate is not promoted |
| Needs tuning | Candidate requires more training work |
| Rollback | Restore previous approved run |