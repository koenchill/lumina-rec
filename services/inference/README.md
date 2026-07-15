# Inference Service

FastAPI service that loads the approved MovieLens model from MLflow and serves predictions.

## Layout

```text
services/inference/
├── app/
│   ├── main.py           # FastAPI routes
│   ├── config.py         # Env-driven settings
│   ├── schemas.py        # Pydantic models
│   ├── auth.py           # API key helpers
│   ├── loading.py        # MLflow download + checksum
│   ├── metrics.py        # Prometheus counters
│   └── logging_utils.py  # Structured JSON logs
├── main.py               # Compatibility re-export of app
├── Dockerfile
├── requirements.txt
└── README.md
```

## Entrypoint

```text
uvicorn services.inference.app.main:app --host 0.0.0.0 --port 8000
```

Shared model and validation code lives in `src/lumina_rec/`.
