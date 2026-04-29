from fastapi.testclient import TestClient

from services.inference.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_endpoint():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_predict_endpoint():
    payload = {"features": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

    response = client.post("/predict", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert "prediction" in body
    assert "model_name" in body
    assert "model_version" in body
    assert "request_id" in body
    assert "latency_ms" in body


def test_predict_rejects_bad_feature_length():
    payload = {"features": [1, 2, 3]}

    response = client.post("/predict", json=payload)

    assert response.status_code == 422