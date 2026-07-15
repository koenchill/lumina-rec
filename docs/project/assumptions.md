# Assumptions

## Purpose

This file records key assumptions for Lumina Rec.

## Technical Assumptions

| Assumption | Reason |
|---|---|
| Local development runs on Windows PowerShell | Current workflow uses PowerShell scripts |
| Docker Desktop is available | Required for Docker Compose stack |
| MLflow is reachable at localhost:5000 | Required for training and local UI |
| MinIO is reachable at localhost:9000 | Required for artifact storage |
| Inference API uses localhost:8001 | Current Docker Compose port mapping |
| MovieLens latest small is acceptable | Fits local recommender demonstration |
| API key auth is enough for local use | Production auth is planned later |
| `.env` is not committed | Protects local credentials |
| Approved model is selected by run ID | Registry alias support is future work |

## Project Assumptions

| Assumption | Reason |
|---|---|
| This is a portfolio and local MLOps project | Design favors learning and demonstration |
| Production controls are documented but not implemented | Local system comes first |
| Documentation is part of the deliverable | Supports reviewer and handoff value |