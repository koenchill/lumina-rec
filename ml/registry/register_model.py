import json
import os
from pathlib import Path

import mlflow
from dotenv import load_dotenv
from mlflow.exceptions import MlflowException
from mlflow.tracking import MlflowClient

load_dotenv()

APPROVED_MODEL_CONFIG_PATH = Path("configs/approved_model.json")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")


def load_approved_model_config() -> dict:
    if not APPROVED_MODEL_CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Missing approved model config: {APPROVED_MODEL_CONFIG_PATH}"
        )

    return json.loads(APPROVED_MODEL_CONFIG_PATH.read_text(encoding="utf-8"))


def ensure_registered_model(
    client: MlflowClient,
    registered_model_name: str,
) -> None:
    try:
        client.create_registered_model(registered_model_name)
        print(f"Created registered model: {registered_model_name}")
    except MlflowException:
        print(f"Registered model already exists: {registered_model_name}")


def register_approved_model() -> None:
    config = load_approved_model_config()

    model_run_id = config["model_run_id"]
    artifact_path = config["model_artifact_path"]
    registered_model_name = config["registered_model_name"]
    model_alias = config["model_alias"]

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

    ensure_registered_model(
        client=client,
        registered_model_name=registered_model_name,
    )

    source = f"runs:/{model_run_id}/{artifact_path}"

    model_version = client.create_model_version(
        name=registered_model_name,
        source=source,
        run_id=model_run_id,
    )

    client.set_registered_model_alias(
        name=registered_model_name,
        alias=model_alias,
        version=model_version.version,
    )

    print("Approved model registered.")
    print(f"Registered model: {registered_model_name}")
    print(f"Model version: {model_version.version}")
    print(f"Alias: {model_alias}")
    print(f"Run ID: {model_run_id}")
    print(f"Source: {source}")


if __name__ == "__main__":
    register_approved_model()