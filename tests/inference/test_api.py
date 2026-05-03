import json
from pathlib import Path

from fastapi.testclient import TestClient

from services.inference.main import app

client = TestClient(app)

API_HEADERS = {"x-api-key": "local-dev-api-key"}

APPROVED_MODEL_CONFIG = json.loads(
    Path("configs/approved_model.json").read_text(encoding="utf-8")
)

APPROVED_MODEL_NAME = APPROVED_MODEL_CONFIG["model_name"]
APPROVED_MODEL_VERSION = APPROVED_MODEL_CONFIG["model_version"]
APPROVED_MODEL_RUN_ID = APPROVED_MODEL_CONFIG["model_run_id"]
APPROVED_MODEL_ARTIFACT_PATH = APPROVED_MODEL_CONFIG["model_artifact_path"]
APPROVED_MODEL_SHA256 = APPROVED_MODEL_CONFIG["model_sha256"]


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_endpoint():
    response = client.get("/ready")
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "ready"
    assert body["model_name"] == APPROVED_MODEL_NAME
    assert body["model_version"] == APPROVED_MODEL_VERSION
    assert body["model_run_id"] == APPROVED_MODEL_RUN_ID
    assert body["model_artifact_path"] == APPROVED_MODEL_ARTIFACT_PATH
    assert body["model_sha256"] == APPROVED_MODEL_SHA256
    assert body["checksum_validation"] == "enabled"
    assert body["movie_metadata_status"] == "loaded"
    assert int(body["movie_metadata_count"]) > 0
    assert body["artifact_manifest_status"] == "validated"
    assert body["artifact_manifest_version"] == "1.0"


def test_version_endpoint():
    response = client.get("/version")
    body = response.json()

    assert response.status_code == 200
    assert body["service_name"] == "lumina-rec-inference"
    assert body["service_version"] == APPROVED_MODEL_VERSION
    assert body["model_name"] == APPROVED_MODEL_NAME
    assert body["model_version"] == APPROVED_MODEL_VERSION


def test_model_endpoint():
    response = client.get("/model")
    body = response.json()

    assert response.status_code == 200
    assert body["model_name"] == APPROVED_MODEL_NAME
    assert body["model_version"] == APPROVED_MODEL_VERSION
    assert body["model_run_id"] == APPROVED_MODEL_RUN_ID
    assert body["model_artifact_path"] == APPROVED_MODEL_ARTIFACT_PATH
    assert body["model_sha256"] == APPROVED_MODEL_SHA256
    assert body["checksum_validation"] == "enabled"
    assert body["artifact_manifest_status"] == "validated"
    assert body["artifact_manifest_version"] == "1.0"
    assert "model_registry_enabled" in body
    assert body["registered_model_name"] == APPROVED_MODEL_NAME
    assert body["model_alias"] == "approved"


def test_movie_metadata_endpoint():
    response = client.get("/movies/1")
    body = response.json()

    assert response.status_code == 200
    assert body["movie_id"] == 1
    assert body["title"] == "Toy Story (1995)"
    assert body["genres"] == "Adventure|Animation|Children|Comedy|Fantasy"


def test_movie_metadata_rejects_unknown_movie_id():
    response = client.get("/movies/999999999")

    assert response.status_code == 404


def test_predict_endpoint():
    payload = {"user_id": 1, "movie_id": 1}

    response = client.post("/predict", json=payload, headers=API_HEADERS)
    body = response.json()

    assert response.status_code == 200
    assert "predicted_rating" in body
    assert body["user_id"] == 1
    assert body["movie_id"] == 1
    assert body["model_name"] == APPROVED_MODEL_NAME
    assert body["model_version"] == APPROVED_MODEL_VERSION
    assert "request_id" in body
    assert "latency_ms" in body


def test_recommend_endpoint():
    payload = {"user_id": 1, "top_n": 10}

    response = client.post("/recommend", json=payload, headers=API_HEADERS)
    body = response.json()

    assert response.status_code == 200
    assert body["user_id"] == 1
    assert len(body["recommendations"]) == 10
    assert body["model_name"] == APPROVED_MODEL_NAME
    assert body["model_version"] == APPROVED_MODEL_VERSION
    assert "request_id" in body
    assert "latency_ms" in body

    first_item = body["recommendations"][0]
    assert "movie_id" in first_item
    assert "title" in first_item
    assert "genres" in first_item
    assert "predicted_rating" in first_item
    assert first_item["title"] != ""
    assert first_item["genres"] != ""


def test_predict_rejects_missing_api_key():
    payload = {"user_id": 1, "movie_id": 1}

    response = client.post("/predict", json=payload)

    assert response.status_code == 401


def test_predict_rejects_bad_api_key():
    payload = {"user_id": 1, "movie_id": 1}

    response = client.post(
        "/predict",
        json=payload,
        headers={"x-api-key": "wrong-key"},
    )

    assert response.status_code == 401


def test_predict_rejects_missing_required_field():
    payload = {"user_id": 1}

    response = client.post("/predict", json=payload, headers=API_HEADERS)

    assert response.status_code == 422


def test_predict_rejects_unknown_user_id():
    payload = {"user_id": 999999999, "movie_id": 1}

    response = client.post("/predict", json=payload, headers=API_HEADERS)

    assert response.status_code == 404


def test_predict_rejects_unknown_movie_id():
    payload = {"user_id": 1, "movie_id": 999999999}

    response = client.post("/predict", json=payload, headers=API_HEADERS)

    assert response.status_code == 404


def test_recommend_rejects_missing_api_key():
    payload = {"user_id": 1, "top_n": 10}

    response = client.post("/recommend", json=payload)

    assert response.status_code == 401


def test_recommend_rejects_bad_api_key():
    payload = {"user_id": 1, "top_n": 10}

    response = client.post(
        "/recommend",
        json=payload,
        headers={"x-api-key": "wrong-key"},
    )

    assert response.status_code == 401


def test_recommend_rejects_unknown_user_id():
    payload = {"user_id": 999999999, "top_n": 10}

    response = client.post("/recommend", json=payload, headers=API_HEADERS)

    assert response.status_code == 404


def test_recommend_rejects_invalid_top_n():
    payload = {"user_id": 1, "top_n": 100}

    response = client.post("/recommend", json=payload, headers=API_HEADERS)

    assert response.status_code == 422


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "lumina_prediction_requests_total" in response.text
    assert "lumina_prediction_errors_total" in response.text
    assert "lumina_prediction_latency_ms" in response.text
    assert "lumina_rate_limit_errors_total" in response.text


def test_metrics_include_rate_limit_counter():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "lumina_rate_limit_errors_total" in response.text