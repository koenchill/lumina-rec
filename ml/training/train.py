import hashlib
import json
import os
import urllib.request
import zipfile
from pathlib import Path

import mlflow
import pandas as pd
import torch
import torch.nn as nn
from dotenv import load_dotenv
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

load_dotenv()

print("Starting MovieLens recommender training...")

DATA_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = Path("ml/models")

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

ZIP_PATH = RAW_DIR / "ml-latest-small.zip"
EXTRACTED_DIR = RAW_DIR / "ml-latest-small"

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv(
    "MLFLOW_EXPERIMENT_NAME",
    "lumina-rec-recommender",
)

EPOCHS = int(os.getenv("TRAINING_EPOCHS", "5"))
BATCH_SIZE = int(os.getenv("TRAINING_BATCH_SIZE", "512"))
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "32"))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", "0.01"))


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


def download_movielens() -> None:
    if ZIP_PATH.exists() and EXTRACTED_DIR.exists():
        print("MovieLens dataset already exists.")
        return

    print("Downloading MovieLens latest small dataset...")
    urllib.request.urlretrieve(DATA_URL, ZIP_PATH)

    print("Extracting MovieLens dataset...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(RAW_DIR)


def calculate_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def prepare_data():
    ratings_path = EXTRACTED_DIR / "ratings.csv"
    movies_path = EXTRACTED_DIR / "movies.csv"

    ratings = pd.read_csv(ratings_path)
    movies = pd.read_csv(movies_path)

    user_ids = sorted(ratings["userId"].unique())
    movie_ids = sorted(ratings["movieId"].unique())

    user_to_idx = {user_id: idx for idx, user_id in enumerate(user_ids)}
    movie_to_idx = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}
    idx_to_movie = {int(idx): int(movie_id) for movie_id, idx in movie_to_idx.items()}

    ratings["user_idx"] = ratings["userId"].map(user_to_idx)
    ratings["movie_idx"] = ratings["movieId"].map(movie_to_idx)

    train_df, test_df = train_test_split(
        ratings,
        test_size=0.2,
        random_state=42,
        stratify=None,
    )

    mapping_payload = {
    "user_to_idx": {str(k): v for k, v in user_to_idx.items()},
    "movie_to_idx": {str(k): v for k, v in movie_to_idx.items()},
    "idx_to_movie": {str(k): v for k, v in idx_to_movie.items()},
}

    mapping_path = MODEL_DIR / "movielens_mappings.json"
    mapping_path.write_text(json.dumps(mapping_payload, indent=2), encoding="utf-8")

    movie_metadata_path = MODEL_DIR / "movies_metadata.csv"
    movies.to_csv(movie_metadata_path, index=False)

    return train_df, test_df, len(user_ids), len(movie_ids), mapping_path, movie_metadata_path


def build_loader(dataframe: pd.DataFrame, batch_size: int) -> DataLoader:
    user_tensor = torch.tensor(dataframe["user_idx"].values, dtype=torch.long)
    movie_tensor = torch.tensor(dataframe["movie_idx"].values, dtype=torch.long)
    rating_tensor = torch.tensor(dataframe["rating"].values, dtype=torch.float32)

    dataset = TensorDataset(user_tensor, movie_tensor, rating_tensor)

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
    )


def evaluate_model(model: nn.Module, dataframe: pd.DataFrame) -> tuple[float, float]:
    model.eval()

    user_tensor = torch.tensor(dataframe["user_idx"].values, dtype=torch.long)
    movie_tensor = torch.tensor(dataframe["movie_idx"].values, dtype=torch.long)
    actual = dataframe["rating"].values

    with torch.no_grad():
        predictions = model(user_tensor, movie_tensor).numpy()

    mse = mean_squared_error(actual, predictions)
    rmse = mse**0.5

    return mse, rmse


def main() -> None:
    download_movielens()

    train_df, test_df, num_users, num_movies, mapping_path, movie_metadata_path = prepare_data()

    train_loader = build_loader(train_df, BATCH_SIZE)

    model = MatrixFactorizationModel(
        num_users=num_users,
        num_movies=num_movies,
        embedding_dim=EMBEDDING_DIM,
    )

    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    with mlflow.start_run(run_name="movielens-matrix-factorization") as run:
        run_id = run.info.run_id

        mlflow.log_param("dataset", "movielens-latest-small")
        mlflow.log_param("model_type", "matrix_factorization")
        mlflow.log_param("framework", "pytorch")
        mlflow.log_param("num_users", num_users)
        mlflow.log_param("num_movies", num_movies)
        mlflow.log_param("embedding_dim", EMBEDDING_DIM)
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("batch_size", BATCH_SIZE)
        mlflow.log_param("learning_rate", LEARNING_RATE)

        for epoch in range(EPOCHS):
            model.train()
            total_loss = 0.0

            for user_batch, movie_batch, rating_batch in train_loader:
                optimizer.zero_grad()

                prediction_batch = model(user_batch, movie_batch)
                loss = loss_function(prediction_batch, rating_batch)

                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            average_loss = total_loss / len(train_loader)
            mlflow.log_metric("train_loss", average_loss, step=epoch)

            print(f"Epoch {epoch + 1}/{EPOCHS}, train_loss={average_loss:.4f}")

        test_mse, test_rmse = evaluate_model(model, test_df)

        mlflow.log_metric("test_mse", test_mse)
        mlflow.log_metric("test_rmse", test_rmse)

        model_path = MODEL_DIR / "recommender_model.pt"

        model_payload = {
            "state_dict": model.state_dict(),
            "num_users": num_users,
            "num_movies": num_movies,
            "embedding_dim": EMBEDDING_DIM,
            "model_name": "lumina-rec-movielens-mf",
            "model_version": "0.2.0",
        }

        torch.save(model_payload, model_path)

        model_sha256 = calculate_sha256(model_path)

        metadata = {
            "run_id": run_id,
            "model_name": "lumina-rec-movielens-mf",
            "model_version": "0.2.0",
            "model_type": "matrix_factorization",
            "dataset": "movielens-latest-small",
            "model_sha256": model_sha256,
            "num_users": num_users,
            "num_movies": num_movies,
            "embedding_dim": EMBEDDING_DIM,
            "test_mse": test_mse,
            "test_rmse": test_rmse,
        }

        metadata_path = MODEL_DIR / "model_metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        latest_run_path = MODEL_DIR / "latest_run.json"
        latest_run_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        mlflow.log_artifact(str(model_path), artifact_path="approved_model")
        mlflow.log_artifact(str(metadata_path), artifact_path="approved_model")
        mlflow.log_artifact(str(mapping_path), artifact_path="approved_model")
        mlflow.log_artifact(str(movie_metadata_path), artifact_path="approved_model")

        print("Training completed and logged to MLflow.")
        print(f"Run ID: {run_id}")
        print(f"Model SHA256: {model_sha256}")
        print(f"Test RMSE: {test_rmse:.4f}")
        print(f"MLflow URL: {MLFLOW_TRACKING_URI}")


if __name__ == "__main__":
    main()