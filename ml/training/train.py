import os
from pathlib import Path

import mlflow
import torch
import torch.nn as nn
from dotenv import load_dotenv

print("✅ Starting MLflow training...")

load_dotenv()

mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow_experiment_name = os.getenv(
    "MLFLOW_EXPERIMENT_NAME",
    "lumina-rec-recommender",
)

mlflow.set_tracking_uri(mlflow_tracking_uri)
mlflow.set_experiment(mlflow_experiment_name)

with mlflow.start_run(run_name="simple-model"):
    mlflow.log_param("model_type", "demo")
    mlflow.log_param("framework", "pytorch")
    mlflow.log_param("layers", "linear")
    mlflow.log_param("input_features", 10)
    mlflow.log_param("output_features", 1)

    model = nn.Linear(10, 1)

    model_dir = Path("ml/models")
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "demo_model.pt"
    torch.save(model.state_dict(), model_path)

    mlflow.log_artifact(str(model_path), artifact_path="model_state_dict")

    print("✅ Training completed and logged to MLflow!")
    print(f"Run URL: {mlflow_tracking_uri}")