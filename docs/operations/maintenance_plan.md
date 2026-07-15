# Maintenance Plan

## Purpose

This document defines routine maintenance for Lumina Rec.

## Daily Checks During Development

| Check | Command |
|---|---|
| Git status | `git status` |
| Running services | `docker compose ps` |
| Inference readiness | `.\scripts\lumina.ps1 ready` |
| Prediction check | `.\scripts\lumina.ps1 predict` |
| Recommendation check | `.\scripts\lumina.ps1 recommend` |
| Tests | `.\scripts\lumina.ps1 test` |

## Weekly Checks

| Check | Purpose |
|---|---|
| Run load test | Confirm performance baseline |
| Review Docker disk usage | Prevent local clutter |
| Review docs | Keep documentation aligned |
| Review dependency versions | Reduce drift |
| Review GitHub Actions | Confirm CI health |

## Model Maintenance

| Task | Trigger |
|---|---|
| Train candidate model | New experiment |
| Compare RMSE | After training |
| Update promotion record | After approval |
| Update rollback values | After approval |
| Run validation | After promotion |

## Docker Maintenance

```powershell
docker system df
docker container prune