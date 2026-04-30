## Architecture Diagram

```mermaid
flowchart LR
    Developer[Developer]
    Train[PyTorch Training Script]
    MLflow[MLflow Tracking Server]
    Postgres[(Postgres Metadata Store)]
    MinIO[(MinIO Artifact Store)]
    Client[Client]
    API[FastAPI Inference API]
    Model[Validated PyTorch Model]
    Metrics[Prometheus Metrics]
    Logs[Structured JSON Logs]

    Developer --> Train
    Train --> MLflow
    MLflow --> Postgres
    MLflow --> MinIO

    Client -->|POST /predict with x-api-key| API
    API -->|loads checksum validated model| Model
    Model --> API
    API --> Client
    API --> Metrics
    API --> Logs