import hashlib
import json
from pathlib import Path

import mlflow
import pandas as pd
import torch
from mlflow.tracking import MlflowClient

from lumina_rec.models import MatrixFactorizationModel
from lumina_rec.validation.artifact_manifest import validate_artifact_manifest
from services.inference.app.config import (
    APPROVED_MODEL_DIR,
    DEFAULT_MODEL_NAME,
    DEFAULT_MODEL_VERSION,
    MLFLOW_TRACKING_URI,
    MODEL_ALIAS,
    MODEL_ARTIFACT_PATH,
    MODEL_RUN_ID,
    MODEL_SHA256,
    REGISTERED_MODEL_NAME,
    USE_MODEL_REGISTRY,
)
from services.inference.app.logging_utils import log_event


def calculate_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def resolve_model_run_id() -> str:
    if MODEL_RUN_ID:
        return MODEL_RUN_ID

    if not USE_MODEL_REGISTRY:
        raise ValueError("MODEL_RUN_ID is required unless USE_MODEL_REGISTRY=true")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

    model_version = client.get_model_version_by_alias(
        name=REGISTERED_MODEL_NAME,
        alias=MODEL_ALIAS,
    )

    if not model_version.run_id:
        raise ValueError(
            f"No run ID found for model alias: {REGISTERED_MODEL_NAME}@{MODEL_ALIAS}"
        )

    return model_version.run_id


def download_approved_artifacts() -> tuple[Path, str]:
    resolved_run_id = resolve_model_run_id()

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    APPROVED_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    artifact_local_path = mlflow.artifacts.download_artifacts(
        run_id=resolved_run_id,
        artifact_path=MODEL_ARTIFACT_PATH,
        dst_path=str(APPROVED_MODEL_DIR),
    )

    return Path(artifact_local_path), resolved_run_id


def load_json(file_path: Path) -> dict:
    return json.loads(file_path.read_text(encoding="utf-8"))


def load_movies_metadata(file_path: Path) -> dict[int, dict[str, str]]:
    movies_metadata_df = pd.read_csv(file_path)

    return {
        int(row["movieId"]): {
            "title": str(row["title"]),
            "genres": str(row["genres"]),
        }
        for _, row in movies_metadata_df.iterrows()
    }


def load_model() -> tuple[MatrixFactorizationModel, dict, dict, dict[int, dict[str, str]], str]:
    artifact_dir, resolved_run_id = download_approved_artifacts()

    model_path = artifact_dir / "recommender_model.pt"
    metadata_path = artifact_dir / "model_metadata.json"
    mappings_path = artifact_dir / "movielens_mappings.json"
    movies_metadata_path = artifact_dir / "movies_metadata.csv"

    if not model_path.exists():
        raise FileNotFoundError(f"Approved model file not found: {model_path}")

    if not metadata_path.exists():
        raise FileNotFoundError(f"Model metadata file not found: {metadata_path}")

    if not mappings_path.exists():
        raise FileNotFoundError(f"MovieLens mappings file not found: {mappings_path}")

    if not movies_metadata_path.exists():
        raise FileNotFoundError(f"Movie metadata file not found: {movies_metadata_path}")

    actual_sha256 = calculate_sha256(model_path)

    if MODEL_SHA256 and actual_sha256 != MODEL_SHA256:
        log_event(
            "model_checksum_failed",
            model_path=str(model_path),
            expected_sha256=MODEL_SHA256,
            actual_sha256=actual_sha256,
            status="error",
        )
        raise ValueError("Model checksum validation failed")

    metadata = load_json(metadata_path)
    mappings = load_json(mappings_path)
    movies_metadata = load_movies_metadata(movies_metadata_path)

    metadata["resolved_model_run_id"] = resolved_run_id

    manifest = validate_artifact_manifest(
        artifact_dir=artifact_dir,
        expected_run_id=resolved_run_id,
    )

    metadata["artifact_manifest_status"] = "validated"
    metadata["artifact_manifest_version"] = manifest.get("manifest_version", "unknown")

    model_payload = torch.load(
        model_path,
        map_location="cpu",
        weights_only=False,
    )

    loaded_model = MatrixFactorizationModel(
        num_users=int(model_payload["num_users"]),
        num_movies=int(model_payload["num_movies"]),
        embedding_dim=int(model_payload["embedding_dim"]),
    )

    loaded_model.load_state_dict(model_payload["state_dict"])
    loaded_model.eval()

    log_event(
        "model_loaded",
        model_name=metadata.get("model_name", DEFAULT_MODEL_NAME),
        model_version=metadata.get("model_version", DEFAULT_MODEL_VERSION),
        model_path=str(model_path),
        model_run_id=resolved_run_id,
        artifact_path=MODEL_ARTIFACT_PATH,
        model_sha256=actual_sha256,
        checksum_validation="enabled" if MODEL_SHA256 else "not_configured",
        model_registry_enabled=str(USE_MODEL_REGISTRY).lower(),
        registered_model_name=REGISTERED_MODEL_NAME,
        model_alias=MODEL_ALIAS,
        movie_metadata_count=len(movies_metadata),
        artifact_manifest_status=metadata.get("artifact_manifest_status"),
        artifact_manifest_version=metadata.get("artifact_manifest_version"),
    )

    return loaded_model, metadata, mappings, movies_metadata, actual_sha256
