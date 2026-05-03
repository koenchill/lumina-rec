from pathlib import Path

import pandas as pd
import pytest

from ml.validation.dataset_checks import (
    validate_columns,
    validate_movie_references,
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


def test_validate_movie_references_passes_when_movies_exist():
    ratings = pd.DataFrame({"movieId": [1, 2, 3]})
    movies = pd.DataFrame({"movieId": [1, 2, 3]})

    validate_movie_references(ratings, movies)


def test_validate_movie_references_raises_for_unknown_movies():
    ratings = pd.DataFrame({"movieId": [1, 2, 999]})
    movies = pd.DataFrame({"movieId": [1, 2, 3]})

    with pytest.raises(ValueError, match="unknown movie IDs"):
        validate_movie_references(ratings, movies)