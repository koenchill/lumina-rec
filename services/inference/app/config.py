import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

MODEL_RUN_ID = os.getenv("MODEL_RUN_ID")
MODEL_ARTIFACT_PATH = os.getenv("MODEL_ARTIFACT_PATH", "approved_model")
MODEL_SHA256 = os.getenv("MODEL_SHA256")

USE_MODEL_REGISTRY = os.getenv("USE_MODEL_REGISTRY", "false").lower() == "true"
REGISTERED_MODEL_NAME = os.getenv("REGISTERED_MODEL_NAME", "lumina-rec-movielens-mf")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "approved")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
APPROVED_MODEL_DIR = Path(os.getenv("APPROVED_MODEL_DIR", "ml/models/approved"))

API_KEY = os.getenv("LUMINA_API_KEY", "local-dev-api-key")
RATE_LIMIT = os.getenv("LUMINA_RATE_LIMIT", "30/minute")

DEFAULT_MODEL_NAME = "lumina-rec-movielens-mf"
DEFAULT_MODEL_VERSION = "0.2.0"
