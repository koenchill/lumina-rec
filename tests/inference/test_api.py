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
    assert body["model_name"] == "lumina-rec-demo-model"
    assert body["model_version"] == "0.1.0"
    assert "model_sha256" in body
    assert body["checksum_validation"] in ["enabled", "not_configured"]


def test_predict_endpoint():
    {"user_id": 1, "movie_id": 1}

    response = client.post("/predict", json=payload, headers=API_HEADERS)
    body = response.json()

    assert response.status_code == 200
    assert "prediction" in body
    assert body["model_name"] == "lumina-rec-demo-model"
    assert body["model_version"] == "0.1.0"
    assert "request_id" in body
    assert "latency_ms" in body


def test_predict_rejects_missing_api_key():
    payload = {"features": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

    response = client.post("/predict", json=payload)

    assert response.status_code == 401


def test_predict_rejects_bad_api_key():
    payload = {"features": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

    response = client.post(
        "/predict",
        json=payload,
        headers={"x-api-key": "wrong-key"},
    )

    assert response.status_code == 401


def test_predict_rejects_bad_feature_length():
    payload = {"features": [1, 2, 3]}

    response = client.post("/predict", json=payload, headers=API_HEADERS)

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