import pandas as pd
import torch
import torch.nn as nn

from ml.evaluation.evaluate_recommender import (
    build_relevant_items_by_user,
    evaluate_ranking_metrics,
)


class DummyRecommender(nn.Module):
    def forward(self, user_idx: torch.Tensor, movie_idx: torch.Tensor) -> torch.Tensor:
        return movie_idx.float()


def test_build_relevant_items_by_user_filters_by_threshold():
    test_df = pd.DataFrame(
        {
            "user_idx": [0, 0, 1, 1],
            "movie_idx": [1, 2, 3, 4],
            "rating": [5.0, 3.0, 4.0, 2.0],
        }
    )

    result = build_relevant_items_by_user(test_df, relevance_threshold=4.0)

    assert result == {0: {1}, 1: {3}}


def test_evaluate_ranking_metrics_returns_expected_keys():
    model = DummyRecommender()

    test_df = pd.DataFrame(
        {
            "user_idx": [0, 0, 1, 1],
            "movie_idx": [1, 4, 2, 3],
            "rating": [5.0, 4.0, 4.0, 5.0],
        }
    )

    result = evaluate_ranking_metrics(
        model=model,
        test_df=test_df,
        num_movies=5,
        k=3,
        relevance_threshold=4.0,
    )

    assert "precision_at_k" in result
    assert "recall_at_k" in result
    assert "ndcg_at_k" in result
    assert "catalog_coverage" in result
    assert "evaluated_users" in result
    assert result["evaluated_users"] == 2.0


def test_evaluate_ranking_metrics_returns_zero_when_no_relevant_items_exist():
    model = DummyRecommender()

    test_df = pd.DataFrame(
        {
            "user_idx": [0, 1],
            "movie_idx": [1, 2],
            "rating": [2.0, 3.0],
        }
    )

    result = evaluate_ranking_metrics(
        model=model,
        test_df=test_df,
        num_movies=5,
        k=3,
        relevance_threshold=4.0,
    )

    assert result["precision_at_k"] == 0.0
    assert result["recall_at_k"] == 0.0
    assert result["ndcg_at_k"] == 0.0
    assert result["catalog_coverage"] == 0.0
    assert result["evaluated_users"] == 0.0