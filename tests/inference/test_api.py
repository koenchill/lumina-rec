from fastapi.testclient import TestClient

from services.inference.main import app

client = TestClient(app)

API_HEADERS = {"x-api-key": "local-dev-api-key"}


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_endpoint():
    response = client.get("/ready")
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "ready"
    assert body["model_name"] == "lumina-rec-movielens-mf"
    assert body["model_version"] == "0.2.0"
    assert body["model_run_id"] == "248c55bf41994c05923a86e354158303"
    assert body["model_artifact_path"] == "approved_model"
    assert "model_sha256" in body
    assert body["checksum_validation"] in ["enabled", "not_configured"]


def test_predict_endpoint():
    payload = {"user_id": 1, "movie_id": 1}

    response = client.post("/predict", json=payload, headers=API_HEADERS)
    body = response.json()

    assert response.status_code == 200
    assert "predicted_rating" in body
    assert body["user_id"] == 1
    assert body["movie_id"] == 1
    assert body["model_name"] == "lumina-rec-movielens-mf"
    assert body["model_version"] == "0.2.0"
    assert "request_id" in body
    assert "latency_ms" in body


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