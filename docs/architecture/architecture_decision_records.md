# Architecture Decision Records

## ADR 001, Use Docker Compose for Local Orchestration

Decision: Use Docker Compose for the local stack.

Reason:

- Simple local setup
- Supports MLflow, MinIO, Postgres, and inference service
- Easy to validate end to end

## ADR 002, Use MLflow for Experiment Tracking

Decision: Use MLflow as the experiment tracker.

Reason:

- Tracks parameters, metrics, and artifacts
- Supports local and future production patterns
- Provides model lineage

## ADR 003, Use MinIO for Local Artifact Storage

Decision: Use MinIO as local S3 compatible artifact storage.

Reason:

- Matches common object storage patterns
- Works with MLflow
- Supports local development without cloud dependency

## ADR 004, Use FastAPI for Inference

Decision: Use FastAPI for the inference service.

Reason:

- Clear API contracts
- Strong request validation with Pydantic
- Easy testing with TestClient
- Good fit for local MLOps APIs

## ADR 005, Use SHA256 for Model Integrity

Decision: Verify approved model artifacts with SHA256.

Reason:

- Detects artifact mismatch
- Reduces model tampering risk
- Supports audit friendly validation

## ADR 006, Use MovieLens Dataset

Decision: Use MovieLens latest small.

Reason:

- Public recommender dataset
- Small enough for local training
- Strong fit for recommendation workflows