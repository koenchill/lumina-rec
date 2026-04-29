FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY ml/models/demo_model.pt ml/models/demo_model.pt
COPY services/inference services/inference

RUN pip install --no-cache-dir fastapi uvicorn torch pydantic

EXPOSE 8000

CMD ["uvicorn", "services.inference.main:app", "--host", "0.0.0.0", "--port", "8000"]