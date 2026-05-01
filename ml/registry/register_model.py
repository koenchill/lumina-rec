import os

import mlflow
from dotenv import load_dotenv
from mlflow.tracking import MlflowClient

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_RUN_ID = os.getenv("MODEL_RUN_ID")
MODEL_ARTIFACT_PATH = os.getenv("MODEL_ARTIFACT_PATH", "approved_model")
REGISTERED_MODEL_NAME = os.getenv(
    "REGISTERED_MODEL_NAME",
    "lumina-rec-movielens-mf",
)
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "approved")


def main() -> None:
    if not MODEL_RUN_ID:
        raise ValueError("MODEL_RUN_ID is required")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

    artifact_uri = f"runs:/{MODEL_RUN_ID}/{MODEL_ARTIFACT_PATH}/recommender_model.pt"

    try:
        client.create_registered_model(REGISTERED_MODEL_NAME)
        print(f"Created registered model: {REGISTERED_MODEL_NAME}")
    except Exception:
        print(f"Registered model already exists: {REGISTERED_MODEL_NAME}")

    model_version = client.create_model_version(
        name=REGISTERED_MODEL_NAME,
        source=artifact_uri,
        run_id=MODEL_RUN_ID,
    )

    client.set_registered_model_alias(
        name=REGISTERED_MODEL_NAME,
        alias=MODEL_ALIAS,
        version=model_version.version,
    )

    print("Model registered successfully.")
    print(f"Registered model: {REGISTERED_MODEL_NAME}")
    print(f"Version: {model_version.version}")
    print(f"Alias: {MODEL_ALIAS}")
    print(f"Run ID: {MODEL_RUN_ID}")
    print(f"Source: {artifact_uri}")


if __name__ == "__main__":
    main()