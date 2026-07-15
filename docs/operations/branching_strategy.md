# Branching Strategy

## Purpose

This document defines a simple branching strategy for Lumina Rec.

## Current Strategy

The current local workflow uses `main` for direct development.

This is acceptable while the project is in solo local development.

## Future Strategy

When the project matures, use feature branches.

## Branch Types

| Branch Type | Example | Purpose |
|---|---|---|
| main | main | Stable working branch |
| feature | feature/movie-lookup | New feature |
| docs | docs/update-runbooks | Documentation updates |
| fix | fix/checksum-validation | Bug fix |
| experiment | experiment/model-tuning | Model experiment |

## Pull Request Rule

Before merging to `main`, validate:

```powershell
.\scripts\lumina.ps1 ready
.\scripts\lumina.ps1 predict
.\scripts\lumina.ps1 recommend
.\scripts\lumina.ps1 movie
.\scripts\lumina.ps1 test