# Model Lifecycle

## Purpose

This file defines the model lifecycle for Lumina Rec.

## Lifecycle Stages

| Stage | Description |
|---|---|
| Data preparation | Download and validate MovieLens data |
| Training | Train matrix factorization model |
| Evaluation | Calculate RMSE and future ranking metrics |
| Artifact logging | Log model, mappings, metadata, and checksum |
| Candidate review | Compare candidate to approved baseline |
| Promotion | Update approved model values |
| Serving | Load approved model into inference API |
| Monitoring | Track latency, errors, and request volume |
| Rollback | Restore previous approved model if needed |

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| RMSE | 2.0162 |

## Promotion Rule

A candidate model should pass tests and show equal or better performance before promotion.