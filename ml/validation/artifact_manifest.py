import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REQUIRED_ARTIFACTS = [
    "recommender_model.pt",
    "model_metadata.json",
    "movielens_mappings.json",
    "movies_metadata.csv",
]


def calculate_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def build_artifact_manifest(
    artifact_dir: Path,
    run_id: str,
    model_name: str,
    model_version: str,
    required_artifacts: list[str] | None = None,
) -> dict[str, Any]:
    required = required_artifacts or DEFAULT_REQUIRED_ARTIFACTS

    manifest = {
        "manifest_version": "1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "model_name": model_name,
        "model_version": model_version,
        "artifacts": {},
    }

    for artifact_name in required:
        artifact_path = artifact_dir / artifact_name

        if not artifact_path.exists():
            raise FileNotFoundError(f"Missing artifact: {artifact_path}")

        manifest["artifacts"][artifact_name] = {
            "sha256": calculate_sha256(artifact_path),
            "size_bytes": artifact_path.stat().st_size,
        }

    return manifest


def write_artifact_manifest(
    artifact_dir: Path,
    run_id: str,
    model_name: str,
    model_version: str,
    manifest_name: str = "artifact_manifest.json",
) -> Path:
    manifest = build_artifact_manifest(
        artifact_dir=artifact_dir,
        run_id=run_id,
        model_name=model_name,
        model_version=model_version,
    )

    manifest_path = artifact_dir / manifest_name
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return manifest_path


def load_artifact_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing artifact manifest: {manifest_path}")

    return json.loads(manifest_path.read_text(encoding="utf-8"))


def validate_artifact_manifest(
    artifact_dir: Path,
    expected_run_id: str | None = None,
    manifest_name: str = "artifact_manifest.json",
) -> dict[str, Any]:
    manifest_path = artifact_dir / manifest_name
    manifest = load_artifact_manifest(manifest_path)

    if expected_run_id and manifest.get("run_id") != expected_run_id:
        raise ValueError(
            f"Artifact manifest run ID mismatch. "
            f"Expected {expected_run_id}, found {manifest.get('run_id')}"
        )

    artifacts = manifest.get("artifacts", {})

    for artifact_name, expected in artifacts.items():
        artifact_path = artifact_dir / artifact_name

        if not artifact_path.exists():
            raise FileNotFoundError(f"Missing artifact: {artifact_path}")

        actual_sha256 = calculate_sha256(artifact_path)
        expected_sha256 = expected.get("sha256")

        if actual_sha256 != expected_sha256:
            raise ValueError(
                f"Artifact checksum mismatch for {artifact_name}. "
                f"Expected {expected_sha256}, found {actual_sha256}"
            )

    return manifest