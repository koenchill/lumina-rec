import hashlib
import json
import os
import sys
import urllib.request
import zipfile
from pathlib import Path

import mlflow
import pandas as pd
import torch
import torch.nn as nn
from dotenv import load_dotenv
from torch.utils.data import DataLoader, TensorDataset

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.validation.artifact_manifest import write_artifact_manifest

load_dotenv()

MOVIELENS_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

DATA_DIR = Path("data/raw")
MOVIELENS_DIR = DATA_DIR / "ml-latest-small"
MOVIELENS_ZIP = DATA_DIR / "ml-latest-small.zip"

MODEL_DIR = Path("ml/models")
LATEST_TRAINING_RUN_PATH = Path("reports/latest_training_run.json")

MODEL_NAME = "lumina-rec-movielens-mf"
MODEL_VERSION = "0.2.0"
MODEL_ARTIFACT_PATH = "approved_model"

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv(
    "MLFLOW_EXPERIMENT_NAME",
    "lumina-rec-recommender",
)

RANDOM_SEED = 42
EMBEDDING_DIM = 32
EPOCHS = 5
BATCH_SIZE = 512
LEARNING_RATE = 0.01


class MatrixFactorizationModel(nn.Module):
    def __init__(self, num_users: int, num_movies: int, embedding_dim: int):
        super().__init__()

        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.movie_embedding = nn.Embedding(num_movies, embedding_dim)
        self.user_bias = nn.Embedding(num_users, 1)
        self.movie_bias = nn.Embedding(num_movies, 1)
        self.global_bias = nn.Parameter(torch.zeros(1))

    def forward(self, user_idx: torch.Tensor, movie_idx: torch.Tensor) -> torch.Tensor:
        user_vector = self.user_embedding(user_idx)
        movie_vector = self.movie_embedding(movie_idx)

        dot_product = (user_vector * movie_vector).sum(dim=1)
        user_bias = self.user_bias(user_idx).squeeze()
        movie_bias = self.movie_bias(movie_idx).squeeze()

        rating = dot_product + user_bias + movie_bias + self.global_bias
        return torch.clamp(rating, min=0.5, max=5.0)


def download_movielens_dataset() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if MOVIELENS_DIR.exists():
        print("MovieLens dataset already exists.")
        return

    print("Downloading MovieLens latest small dataset...")
    urllib.request.urlretrieve(MOVIELENS_URL, MOVIELENS_ZIP)

    print("Extracting MovieLens dataset...")
    with zipfile.ZipFile(MOVIELENS_ZIP, "r") as zip_ref:
        zip_ref.extractall(DATA_DIR)


def calculate_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def write_json(file_path: Path, payload: dict) -> None:
    file_path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )


def write_latest_training_run(
    run_id: str,
    model_sha256: str,
    test_rmse: float,
    model_name: str,
    model_version: str,
    artifact_path: str,
) -> None:
    LATEST_TRAINING_RUN_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "model_name": model_name,
        "model_version": model_version,
        "model_run_id": run_id,
        "model_sha256": model_sha256,
        "model_artifact_path": artifact_path,
        "test_rmse": round(float(test_rmse), 4),
        "registered_model_name": model_name,
        "model_alias": "approved",
    }

    LATEST_TRAINING_RUN_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )


def prepare_data() -> tuple[pd.DataFrame, pd.DataFrame, int, int, Path, Path]:
    download_movielens_dataset()

    ratings_path = MOVIELENS_DIR / "ratings.csv"
    movies_path = MOVIELENS_DIR / "movies.csv"

    ratings = pd.read_csv(ratings_path)
    movies = pd.read_csv(movies_path)

    user_ids = sorted(int(user_id) for user_id in ratings["userId"].unique())
    movie_ids = sorted(int(movie_id) for movie_id in ratings["movieId"].unique())

    user_to_idx_int = {user_id: idx for idx, user_id in enumerate(user_ids)}
    movie_to_idx_int = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}

    user_to_idx = {str(user_id): int(idx) for user_id, idx in user_to_idx_int.items()}
    movie_to_idx = {str(movie_id): int(idx) for movie_id, idx in movie_to_idx_int.items()}
    idx_to_movie = {str(idx): int(movie_id) for movie_id, idx in movie_to_idx_int.items()}

    ratings["user_idx"] = ratings["userId"].astype(int).map(user_to_idx_int)
    ratings["movie_idx"] = ratings["movieId"].astype(int).map(movie_to_idx_int)

    ratings = ratings.dropna(subset=["user_idx", "movie_idx", "rating"]).copy()
    ratings["user_idx"] = ratings["user_idx"].astype(int)
    ratings["movie_idx"] = ratings["movie_idx"].astype(int)
    ratings["rating"] = ratings["rating"].astype(float)

    train_df = ratings.sample(frac=0.8, random_state=RANDOM_SEED)
    test_df = ratings.drop(train_df.index)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    mapping_payload = {
        "user_to_idx": user_to_idx,
        "movie_to_idx": movie_to_idx,
        "idx_to_movie": idx_to_movie,
    }

    mapping_path = MODEL_DIR / "movielens_mappings.json"
    write_json(mapping_path, mapping_payload)

    movie_metadata_path = MODEL_DIR / "movies_metadata.csv"
    movies.to_csv(movie_metadata_path, index=False)

    return (
        train_df,
        test_df,
        len(user_ids),
        len(movie_ids),
        mapping_path,
        movie_metadata_path,
    )


def build_dataloader(dataframe: pd.DataFrame, shuffle: bool) -> DataLoader:
    user_tensor = torch.tensor(dataframe["user_idx"].values, dtype=torch.long)
    movie_tensor = torch.tensor(dataframe["movie_idx"].values, dtype=torch.long)
    rating_tensor = torch.tensor(dataframe["rating"].values, dtype=torch.float32)

    dataset = TensorDataset(user_tensor, movie_tensor, rating_tensor)

    return DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=shuffle,
    )


def train_model(
    model: MatrixFactorizationModel,
    train_loader: DataLoader,
) -> None:
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    loss_function = nn.MSELoss()

    model.train()

    for epoch in range(EPOCHS):
        total_loss = 0.0

        for user_idx, movie_idx, rating in train_loader:
            optimizer.zero_grad()

            prediction = model(user_idx, movie_idx)
            loss = loss_function(prediction, rating)

            loss.backward()
            optimizer.step()

            total_loss += float(loss.item())

        average_loss = total_loss / max(len(train_loader), 1)
        print(f"Epoch {epoch + 1}/{EPOCHS}, train_loss={average_loss:.4f}")


def evaluate_model(
    model: MatrixFactorizationModel,
    test_loader: DataLoader,
) -> float:
    model.eval()

    squared_errors = []
    with torch.no_grad():
        for user_idx, movie_idx, rating in test_loader:
            prediction = model(user_idx, movie_idx)
            squared_error = (prediction - rating) ** 2
            squared_errors.extend(squared_error.tolist())

    mse = sum(squared_errors) / max(len(squared_errors), 1)
    return mse**0.5


def save_model_payload(
    model: MatrixFactorizationModel,
    num_users: int,
    num_movies: int,
) -> Path:
    model_path = MODEL_DIR / "recommender_model.pt"

    payload = {
        "state_dict": model.state_dict(),
        "num_users": int(num_users),
        "num_movies": int(num_movies),
        "embedding_dim": int(EMBEDDING_DIM),
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
    }

    torch.save(payload, model_path)

    return model_path


def main() -> None:
    print("Starting MovieLens recommender training...")

    torch.manual_seed(RANDOM_SEED)

    (
        train_df,
        test_df,
        num_users,
        num_movies,
        mapping_path,
        movie_metadata_path,
    ) = prepare_data()

    train_loader = build_dataloader(train_df, shuffle=True)
    test_loader = build_dataloader(test_df, shuffle=False)

    model = MatrixFactorizationModel(
        num_users=num_users,
        num_movies=num_movies,
        embedding_dim=EMBEDDING_DIM,
    )

    train_model(model, train_loader)
    test_rmse = evaluate_model(model, test_loader)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    with mlflow.start_run(run_name="movielens-matrix-factorization") as run:
        model_path = save_model_payload(
            model=model,
            num_users=num_users,
            num_movies=num_movies,
        )

        model_sha256 = calculate_sha256(model_path)

        metadata = {
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION,
            "model_type": "matrix_factorization",
            "framework": "pytorch",
            "dataset": "MovieLens latest small",
            "run_id": run.info.run_id,
            "artifact_path": MODEL_ARTIFACT_PATH,
            "model_sha256": model_sha256,
            "test_rmse": round(float(test_rmse), 4),
            "num_users": int(num_users),
            "num_movies": int(num_movies),
            "embedding_dim": int(EMBEDDING_DIM),
            "epochs": int(EPOCHS),
            "batch_size": int(BATCH_SIZE),
            "learning_rate": float(LEARNING_RATE),
            "required_artifacts": [
                model_path.name,
                "model_metadata.json",
                mapping_path.name,
                movie_metadata_path.name,
                "artifact_manifest.json",
            ],
        }

        metadata_path = MODEL_DIR / "model_metadata.json"
        write_json(metadata_path, metadata)

        manifest_path = write_artifact_manifest(
            artifact_dir=MODEL_DIR,
            run_id=run.info.run_id,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
        )

        mlflow.log_param("model_name", MODEL_NAME)
        mlflow.log_param("model_version", MODEL_VERSION)
        mlflow.log_param("model_type", "matrix_factorization")
        mlflow.log_param("dataset", "MovieLens latest small")
        mlflow.log_param("embedding_dim", EMBEDDING_DIM)
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("batch_size", BATCH_SIZE)
        mlflow.log_param("learning_rate", LEARNING_RATE)

        mlflow.log_metric("test_rmse", float(test_rmse))

        mlflow.log_artifacts(str(MODEL_DIR), artifact_path=MODEL_ARTIFACT_PATH)

        write_latest_training_run(
            run_id=run.info.run_id,
            model_sha256=model_sha256,
            test_rmse=test_rmse,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
            artifact_path=MODEL_ARTIFACT_PATH,
        )

        print("Training completed and logged to MLflow.")
        print(f"Run ID: {run.info.run_id}")
        print(f"Model SHA256: {model_sha256}")
        print(f"Test RMSE: {test_rmse:.4f}")
        print(f"Manifest: {manifest_path}")
        print(f"Latest training run: {LATEST_TRAINING_RUN_PATH}")
        print(f"MLflow URL: {MLFLOW_TRACKING_URI}")


if __name__ == "__main__":
    main()