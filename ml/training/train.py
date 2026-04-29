import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
from pathlib import Path

print("✅ Starting MLflow training...")

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("lumina-rec-recommender")

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
    #mlflow.pytorch.log_model(model, artifact_path="pytorch_model")

    print("✅ Training completed and logged to MLflow!")
    print("Run URL: http://localhost:5000")