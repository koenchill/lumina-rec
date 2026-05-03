import pytest

from ml.evaluation.ranking_metrics import (
    catalog_coverage,
    dcg_at_k,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)


def test_precision_at_k_returns_expected_value():
    recommended_items = [1, 2, 3, 4, 5]
    relevant_items = {2, 4, 6}

    result = precision_at_k(recommended_items, relevant_items, k=5)

    assert result == 0.4


def test_recall_at_k_returns_expected_value():
    recommended_items = [1, 2, 3, 4, 5]
    relevant_items = {2, 4, 6}

    result = recall_at_k(recommended_items, relevant_items, k=5)

    assert round(result, 4) == 0.6667


def test_dcg_at_k_returns_positive_score_for_relevant_items():
    recommended_items = [1, 2, 3]
    relevant_items = {1, 3}

    result = dcg_at_k(recommended_items, relevant_items, k=3)

    assert result > 0


def test_ndcg_at_k_returns_one_for_ideal_ranking():
    recommended_items = [1, 2, 3]
    relevant_items = {1, 2, 3}

    result = ndcg_at_k(recommended_items, relevant_items, k=3)

    assert result == 1.0


def test_ndcg_at_k_returns_zero_when_no_relevant_items_exist():
    recommended_items = [1, 2, 3]
    relevant_items = set()

    result = ndcg_at_k(recommended_items, relevant_items, k=3)

    assert result == 0.0


def test_catalog_coverage_returns_expected_value():
    recommended_items_by_user = {
        1: [1, 2],
        2: [2, 3],
        3: [4],
    }
    catalog_items = {1, 2, 3, 4, 5}

    result = catalog_coverage(recommended_items_by_user, catalog_items)

    assert result == 0.8


def test_metrics_raise_for_invalid_k():
    with pytest.raises(ValueError, match="k must be greater than 0"):
        precision_at_k([1, 2, 3], {1}, k=0)

    with pytest.raises(ValueError, match="k must be greater than 0"):
        recall_at_k([1, 2, 3], {1}, k=0)

    with pytest.raises(ValueError, match="k must be greater than 0"):
        ndcg_at_k([1, 2, 3], {1}, k=0)