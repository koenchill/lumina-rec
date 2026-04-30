import os

from locust import HttpUser, between, task

API_KEY = os.getenv("LUMINA_API_KEY", "local-dev-api-key")
API_HEADERS = {"x-api-key": API_KEY}


class InferenceUser(HttpUser):
    wait_time = between(0.5, 2)

    @task
    def predict(self):
        payload = {"features": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

        with self.client.post(
            "/predict",
            json=payload,
            headers=API_HEADERS,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
                return

            body = response.json()

            required_fields = [
                "prediction",
                "model_name",
                "model_version",
                "request_id",
                "latency_ms",
            ]

            missing_fields = [field for field in required_fields if field not in body]

            if missing_fields:
                response.failure(f"Missing fields: {missing_fields}")
            else:
                response.success()

    @task(1)
    def health(self):
        self.client.get("/health")