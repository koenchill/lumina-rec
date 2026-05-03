import os

import mlflow
from dotenv import load_dotenv
from mlflow.tracking import MlflowClient

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
REGISTERED_MODEL_NAME = os.getenv(
    "REGISTERED_MODEL_NAME",
    "lumina-rec-movielens-mf",
)
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "approved")


def resolve_model_run_id(
    registered_model_name: str = REGISTERED_MODEL_NAME,
    model_alias: str = MODEL_ALIAS,
    tracking_uri: str = MLFLOW_TRACKING_URI,
) -> str:
    mlflow.set_tracking_uri(tracking_uri)

    client = MlflowClient(tracking_uri=tracking_uri)

    model_version = client.get_model_version_by_alias(
        name=registered_model_name,
        alias=model_alias,
    )

    if not model_version.run_id:
        raise ValueError(
            f"No run ID found for model alias: {registered_model_name}@{model_alias}"
        )

    return model_version.run_id


if __name__ == "__main__":
    run_id = resolve_model_run_id()
    print(f"Resolved run ID: {run_id}")