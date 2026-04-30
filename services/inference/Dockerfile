FROM python:3.11-slim

WORKDIR /app

COPY services/inference/requirements.txt services/inference/requirements.txt
COPY ml/models/demo_model.pt ml/models/demo_model.pt
COPY services/inference services/inference

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cpu \
        torch==2.11.0 && \
    pip install --no-cache-dir \
        -r services/inference/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "services.inference.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--timeout-keep-alive", "30"]