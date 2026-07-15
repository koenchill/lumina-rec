# Stakeholder Handoff

## Purpose

This document summarizes Lumina Rec for stakeholders.

## Project Summary

Lumina Rec is a local MLOps recommendation system that trains a MovieLens recommender, tracks experiments in MLflow, stores model artifacts in MinIO, and serves predictions through FastAPI.

## Current Capabilities

| Capability | Status |
|---|---|
| MovieLens model training | Complete |
| MLflow tracking | Complete |
| MinIO artifact storage | Complete |
| Postgres metadata store | Complete |
| FastAPI inference | Complete |
| `/predict` endpoint | Complete |
| `/recommend` endpoint | Complete |
| `/movies/{movie_id}` endpoint | Complete |
| Model checksum validation | Complete |
| API tests | Complete |
| Load testing | Complete |
| Documentation | In progress |

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Key Value

The project shows how to reduce model deployment risk through approved artifacts, checksum validation, API testing, load testing, rollback planning, and operational runbooks.

## Next Recommended Work

- Add MLflow Model Registry alias loading.
- Add dataset checksum validation.
- Add artifact manifest validation.
- Add ranking quality metrics.
- Add production deployment design.