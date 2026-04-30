# Lumina Rec Architecture

## Purpose

Lumina Rec is a local MLOps recommendation system that demonstrates model training, experiment tracking, artifact storage, containerized inference, observability, and security controls.

## High Level Flow

```text
Developer
   |
   | runs training
   v
PyTorch Training Script
   |
   | logs params, metrics, and artifacts
   v
MLflow Tracking Server
   |
   | stores metadata
   v
Postgres
   |
   | stores artifacts
   v
MinIO

Client
   |
   | POST /predict with x-api-key
   v
FastAPI Inference API
   |
   | loads validated model artifact
   v
PyTorch Model
   |
   | returns prediction response
   v
Client