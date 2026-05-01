# CI CD Strategy

## Purpose

This document explains the CI CD strategy for Lumina Rec.

## Current CI Goals

The CI pipeline should validate:

| Check | Purpose |
|---|---|
| Python tests | Confirm API behavior |
| Docker build | Confirm inference image builds |
| Secret scan | Detect accidental secret exposure |
| Container scan | Detect image vulnerabilities |
| Health check | Confirm service starts |
| Readiness check | Confirm approved model metadata loads |
| Prediction check | Confirm `/predict` works |
| Recommendation check | Confirm `/recommend` works |

## Current Local Validation Commands

```powershell
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend