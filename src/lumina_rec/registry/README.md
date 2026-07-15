# MLflow Registry Utilities

## Purpose

This folder stores utilities for MLflow Model Registry workflows.

## Current Goal

The project currently selects the approved model by MLflow run ID.

Future work will support approved model selection through MLflow Model Registry alias.

## Planned Workflow

1. Train candidate model.
2. Log model artifacts to MLflow.
3. Register model version.
4. Assign alias `approved`.
5. Configure inference to resolve the approved model through the registry alias.
6. Validate `/ready`, `/predict`, `/recommend`, `/movies/{movie_id}`, and tests.

## Expected Values

| Field | Value |
|---|---|
| Registered model name | lumina-rec-movielens-mf |
| Alias | approved |
| Artifact path | approved_model |