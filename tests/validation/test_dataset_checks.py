from pathlib import Path

import pandas as pd
import pytest

from ml.validation.dataset_checks import (
    build_validation_summary,
    validate_columns,
    validate_missing_values,
    validate_movie_references,
    validate_movielens_dataset,
    validate_rating_range,
)


def test_validate_columns_passes_when_required_columns_exist():
    dataframe = pd.DataFrame(
        {
            "userId": [1],
            "movieId": [1],
            "rating": [5.0],
            "timestamp": [123456789],
        }
    )

    validate_columns(
        dataframe=dataframe,
        required_columns={"userId", "movieId", "rating", "timestamp"},
        name="ratings.csv",
    )


def test_validate_columns_raises_when_required_column_is_missing():
    dataframe = pd.DataFrame(
        {
            "userId": [1],
            "movieId": [1],
            "rating": [5.0],
        }
    )

    with pytest.raises(ValueError, match="missing required columns"):
        validate_columns(
            dataframe=dataframe,
            required_columns={"userId", "movieId", "rating", "timestamp"},
            name="ratings.csv",
        )


def test_validate_rating_range_passes_for_valid_ratings():
    ratings = pd.DataFrame({"rating": [0.5, 3.0, 5.0]})

    validate_rating_range(ratings)


def test_validate_rating_range_raises_for_invalid_ratings():
    ratings = pd.DataFrame({"rating": [0.0, 3.0, 5.5]})

    with pytest.raises(ValueError, match="outside the expected"):
        validate_rating_range(ratings)


def test_validate_missing_values_passes_when_required_values_exist():
    ratings = pd.DataFrame(
        {
            "userId": [1],
            "movieId": [1],
            "rating": [5.0],
        }
    )
    movies = pd.DataFrame(
        {
            "movieId": [1],
            "title": ["Toy Story (1995)"],
            "genres": ["Adventure|Animation|Children|Comedy|Fantasy"],
        }
    )

    validate_missing_values(ratings, movies)


def test_validate_missing_values_raises_for_missing_values():
    ratings = pd.DataFrame(
        {
            "userId": [1],
            "movieId": [1],
            "rating": [None],
        }
    )
    movies = pd.DataFrame(
        {
            "movieId": [1],
            "title": ["Toy Story (1995)"],
            "genres": ["Adventure|Animation|Children|Comedy|Fantasy"],
        }
    )

    with pytest.raises(ValueError, match="missing values"):
        validate_missing_values(ratings, movies)


def test_validate_movie_references_passes_when_movies_exist():
    ratings = pd.DataFrame({"movieId": [1, 2, 3]})
    movies = pd.DataFrame({"movieId": [1, 2, 3]})

    validate_movie_references(ratings, movies)


def test_validate_movie_references_raises_for_unknown_movies():
    ratings = pd.DataFrame({"movieId": [1, 2, 999]})
    movies = pd.DataFrame({"movieId": [1, 2, 3]})

    with pytest.raises(ValueError, match="unknown movie IDs"):
        validate_movie_references(ratings, movies)


def test_build_validation_summary_returns_expected_counts():
    ratings = pd.DataFrame(
        {
            "userId": [1, 1, 2],
            "movieId": [1, 2, 2],
            "rating": [5.0, 4.0, 3.0],
        }
    )
    movies = pd.DataFrame(
        {
            "movieId": [1, 2],
            "title": ["Toy Story (1995)", "Jumanji (1995)"],
            "genres": [
                "Adventure|Animation|Children|Comedy|Fantasy",
                "Adventure|Children|Fantasy",
            ],
        }
    )

    summary = build_validation_summary(ratings, movies)

    assert summary["ratings_count"] == 3
    assert summary["movies_count"] == 2
    assert summary["unique_users"] == 2
    assert summary["unique_rated_movies"] == 2
    assert summary["minimum_rating"] == 3.0
    assert summary["maximum_rating"] == 5.0
    assert summary["average_rating"] == 4.0


def test_validate_movielens_dataset_writes_report(tmp_path: Path):
    dataset_dir = tmp_path / "ml-latest-small"
    dataset_dir.mkdir()

    ratings = pd.DataFrame(
        {
            "userId": [1, 2],
            "movieId": [1, 2],
            "rating": [5.0, 4.0],
            "timestamp": [123456789, 123456790],
        }
    )
    movies = pd.DataFrame(
        {
            "movieId": [1, 2],
            "title": ["Toy Story (1995)", "Jumanji (1995)"],
            "genres": [
                "Adventure|Animation|Children|Comedy|Fantasy",
                "Adventure|Children|Fantasy",
            ],
        }
    )

    ratings.to_csv(dataset_dir / "ratings.csv", index=False)
    movies.to_csv(dataset_dir / "movies.csv", index=False)

    report_path = tmp_path / "dataset_validation_report.md"

    summary = validate_movielens_dataset(
        dataset_dir=dataset_dir,
        report_path=report_path,
    )

    assert summary["ratings_count"] == 2
    assert report_path.exists()
    report_content = report_path.read_text(encoding="utf-8")
    assert "Dataset Validation Report" in report_content
    assert "Passed" in report_content