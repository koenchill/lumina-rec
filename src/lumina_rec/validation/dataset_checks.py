from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


REQUIRED_RATINGS_COLUMNS = {"userId", "movieId", "rating", "timestamp"}
REQUIRED_MOVIES_COLUMNS = {"movieId", "title", "genres"}

DEFAULT_DATASET_DIR = Path("data/raw/ml-latest-small")
DEFAULT_REPORT_PATH = Path("reports/dataset_validation_report.md")


def validate_columns(
    dataframe: pd.DataFrame,
    required_columns: set[str],
    name: str,
) -> None:
    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"{name} is missing required columns: {sorted(missing_columns)}"
        )


def validate_rating_range(ratings: pd.DataFrame) -> None:
    invalid_ratings = ratings[
        (ratings["rating"] < 0.5) | (ratings["rating"] > 5.0)
    ]

    if not invalid_ratings.empty:
        raise ValueError(
            "ratings.csv contains ratings outside the expected 0.5 to 5.0 range"
        )


def validate_missing_values(ratings: pd.DataFrame, movies: pd.DataFrame) -> None:
    required_rating_fields = ["userId", "movieId", "rating"]
    required_movie_fields = ["movieId", "title", "genres"]

    missing_rating_values = ratings[required_rating_fields].isna().sum()
    missing_movie_values = movies[required_movie_fields].isna().sum()

    rating_failures = missing_rating_values[missing_rating_values > 0]
    movie_failures = missing_movie_values[missing_movie_values > 0]

    if not rating_failures.empty:
        raise ValueError(
            f"ratings.csv contains missing values: {rating_failures.to_dict()}"
        )

    if not movie_failures.empty:
        raise ValueError(
            f"movies.csv contains missing values: {movie_failures.to_dict()}"
        )


def validate_movie_references(ratings: pd.DataFrame, movies: pd.DataFrame) -> None:
    rating_movie_ids = set(ratings["movieId"].unique())
    movie_ids = set(movies["movieId"].unique())

    missing_movie_ids = rating_movie_ids - movie_ids

    if missing_movie_ids:
        sample = sorted(list(missing_movie_ids))[:10]
        raise ValueError(f"ratings.csv references unknown movie IDs: {sample}")


def build_validation_summary(ratings: pd.DataFrame, movies: pd.DataFrame) -> dict:
    return {
        "ratings_count": int(len(ratings)),
        "movies_count": int(len(movies)),
        "unique_users": int(ratings["userId"].nunique()),
        "unique_rated_movies": int(ratings["movieId"].nunique()),
        "minimum_rating": float(ratings["rating"].min()),
        "maximum_rating": float(ratings["rating"].max()),
        "average_rating": round(float(ratings["rating"].mean()), 4),
    }


def write_validation_report(summary: dict, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    validation_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    content = f"""# Dataset Validation Report

## Status

Passed

## Validation Time

{validation_time}

## Dataset

MovieLens latest small

## Summary

| Metric | Value |
|---|---:|
| Ratings count | {summary["ratings_count"]} |
| Movies count | {summary["movies_count"]} |
| Unique users | {summary["unique_users"]} |
| Unique rated movies | {summary["unique_rated_movies"]} |
| Minimum rating | {summary["minimum_rating"]} |
| Maximum rating | {summary["maximum_rating"]} |
| Average rating | {summary["average_rating"]} |

## Checks Completed

| Check | Result |
|---|---|
| ratings.csv exists | Passed |
| movies.csv exists | Passed |
| ratings.csv required columns exist | Passed |
| movies.csv required columns exist | Passed |
| Required fields have no missing values | Passed |
| Ratings are within 0.5 to 5.0 | Passed |
| Rating movie IDs exist in movies.csv | Passed |
"""

    report_path.write_text(content, encoding="utf-8")


def validate_movielens_dataset(
    dataset_dir: Path = DEFAULT_DATASET_DIR,
    report_path: Path = DEFAULT_REPORT_PATH,
) -> dict:
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
    validate_missing_values(ratings, movies)
    validate_rating_range(ratings)
    validate_movie_references(ratings, movies)

    summary = build_validation_summary(ratings, movies)
    write_validation_report(summary, report_path)

    print("MovieLens dataset validation passed.")
    print(f"Report written to: {report_path}")

    return summary


if __name__ == "__main__":
    validate_movielens_dataset()