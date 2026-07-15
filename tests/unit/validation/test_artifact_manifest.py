import json
from pathlib import Path

import pytest

from lumina_rec.validation.artifact_manifest import (
    build_artifact_manifest,
    calculate_sha256,
    validate_artifact_manifest,
    write_artifact_manifest,
)


def write_test_artifacts(artifact_dir: Path) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)

    (artifact_dir / "recommender_model.pt").write_text("model", encoding="utf-8")
    (artifact_dir / "model_metadata.json").write_text("{}", encoding="utf-8")
    (artifact_dir / "movielens_mappings.json").write_text("{}", encoding="utf-8")
    (artifact_dir / "movies_metadata.csv").write_text(
        "movieId,title,genres\n1,Toy Story (1995),Adventure\n",
        encoding="utf-8",
    )


def test_calculate_sha256_returns_hash(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello", encoding="utf-8")

    result = calculate_sha256(file_path)

    assert len(result) == 64


def test_build_artifact_manifest_includes_required_artifacts(tmp_path: Path):
    artifact_dir = tmp_path / "approved_model"
    write_test_artifacts(artifact_dir)

    manifest = build_artifact_manifest(
        artifact_dir=artifact_dir,
        run_id="run-123",
        model_name="lumina-rec-movielens-mf",
        model_version="0.2.0",
    )

    assert manifest["run_id"] == "run-123"
    assert manifest["model_name"] == "lumina-rec-movielens-mf"
    assert manifest["model_version"] == "0.2.0"
    assert "recommender_model.pt" in manifest["artifacts"]
    assert "model_metadata.json" in manifest["artifacts"]
    assert "movielens_mappings.json" in manifest["artifacts"]
    assert "movies_metadata.csv" in manifest["artifacts"]


def test_write_and_validate_artifact_manifest_passes(tmp_path: Path):
    artifact_dir = tmp_path / "approved_model"
    write_test_artifacts(artifact_dir)

    write_artifact_manifest(
        artifact_dir=artifact_dir,
        run_id="run-123",
        model_name="lumina-rec-movielens-mf",
        model_version="0.2.0",
    )

    manifest = validate_artifact_manifest(
        artifact_dir=artifact_dir,
        expected_run_id="run-123",
    )

    assert manifest["run_id"] == "run-123"


def test_validate_artifact_manifest_fails_on_wrong_run_id(tmp_path: Path):
    artifact_dir = tmp_path / "approved_model"
    write_test_artifacts(artifact_dir)

    write_artifact_manifest(
        artifact_dir=artifact_dir,
        run_id="run-123",
        model_name="lumina-rec-movielens-mf",
        model_version="0.2.0",
    )

    with pytest.raises(ValueError, match="run ID mismatch"):
        validate_artifact_manifest(
            artifact_dir=artifact_dir,
            expected_run_id="wrong-run",
        )


def test_validate_artifact_manifest_fails_on_checksum_mismatch(tmp_path: Path):
    artifact_dir = tmp_path / "approved_model"
    write_test_artifacts(artifact_dir)

    write_artifact_manifest(
        artifact_dir=artifact_dir,
        run_id="run-123",
        model_name="lumina-rec-movielens-mf",
        model_version="0.2.0",
    )

    (artifact_dir / "recommender_model.pt").write_text(
        "tampered model",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="checksum mismatch"):
        validate_artifact_manifest(
            artifact_dir=artifact_dir,
            expected_run_id="run-123",
        )


def test_validate_artifact_manifest_fails_when_manifest_missing(tmp_path: Path):
    artifact_dir = tmp_path / "approved_model"
    write_test_artifacts(artifact_dir)

    with pytest.raises(FileNotFoundError, match="Missing artifact manifest"):
        validate_artifact_manifest(artifact_dir=artifact_dir)


def test_validate_artifact_manifest_fails_when_artifact_missing(tmp_path: Path):
    artifact_dir = tmp_path / "approved_model"
    write_test_artifacts(artifact_dir)

    manifest_path = write_artifact_manifest(
        artifact_dir=artifact_dir,
        run_id="run-123",
        model_name="lumina-rec-movielens-mf",
        model_version="0.2.0",
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    (artifact_dir / "movies_metadata.csv").unlink()
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="Missing artifact"):
        validate_artifact_manifest(
            artifact_dir=artifact_dir,
            expected_run_id="run-123",
        )