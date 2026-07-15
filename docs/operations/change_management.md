# Change Management

## Purpose

This document defines the change management approach for Lumina Rec.

## Change Types

| Change Type | Example |
|---|---|
| Code change | Modify inference endpoint |
| Model change | Promote new MLflow run |
| Config change | Update rate limit |
| Documentation change | Update API contract |
| Dependency change | Update requirements |
| Infrastructure change | Modify Docker Compose or future Terraform |

## Required Checks

| Change | Required Validation |
|---|---|
| API change | API tests and docs update |
| Model change | Promotion checklist and rollback values |
| Config change | Runtime validation |
| Dependency change | Tests and container build |
| Infrastructure change | Docker Compose validation |
| Documentation change | Link and consistency check |

## Standard Validation

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 test
git status