from pathlib import Path

import pandas as pd


REQUIRED_RATINGS_COLUMNS = {"userId", "movieId", "rating", "timestamp"}
REQUIRED_MOVIES_COLUMNS = {"movieId", "title", "genres"}


def validate_columns(dataframe: pd.DataFrame, required_columns: set[str], name: str) -> None:
    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(f"{name} is missing required columns: {sorted(missing_columns)}")


def validate_rating_range(ratings: pd.DataFrame) -> None:
    invalid_ratings = ratings[
        (ratings["rating"] < 0.5) | (ratings["rating"] > 5.0)
    ]

    if not invalid_ratings.empty:
        raise ValueError("ratings.csv contains ratings outside the expected 0.5 to 5.0 range")


def validate_movie_references(ratings: pd.DataFrame, movies: pd.DataFrame) -> None:
    rating_movie_ids = set(ratings["movieId"].unique())
    movie_ids = set(movies["movieId"].unique())

    missing_movie_ids = rating_movie_ids - movie_ids

    if missing_movie_ids:
        sample = sorted(list(missing_movie_ids))[:10]
        raise ValueError(f"ratings.csv references unknown movie IDs: {sample}")


def validate_movielens_dataset(dataset_dir: Path) -> None:
    ratings_path = dataset_dir / "ratings.csv"
    movies_path = dataset_dir / "movies.csv"

    if not ratings_path.exists():
        raise FileNotFoundError(f"Missing ratings file: {ratings_path}")

    if not movies_path.exists():
        raise FileNotFoundError(f"Missing movies file: {movies_path}")

    ratings = pd.read_csv(ratings_path)
    movies = pd.read_csv(movies_path)

    validate_columns(ratings, REQUIRED_RATINGS_COLUMNS, "ratings.csv")
    validate_columns(movies, REQUIRED_MOVIES_COLUMNS, "movies.csv")
    validate_rating_range(ratings)
    validate_movie_references(ratings, movies)

    print("MovieLens dataset validation passed.")


if __name__ == "__main__":
    validate_movielens_dataset(Path("data/raw/ml-latest-small"))