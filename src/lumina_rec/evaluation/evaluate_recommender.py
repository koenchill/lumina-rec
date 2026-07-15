from collections import defaultdict

import pandas as pd
import torch

from lumina_rec.evaluation.ranking_metrics import (
    catalog_coverage,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)


def build_relevant_items_by_user(
    test_df: pd.DataFrame,
    relevance_threshold: float = 4.0,
) -> dict[int, set[int]]:
    relevant_items_by_user: dict[int, set[int]] = defaultdict(set)

    relevant_rows = test_df[test_df["rating"] >= relevance_threshold]

    for row in relevant_rows.itertuples(index=False):
        relevant_items_by_user[int(row.user_idx)].add(int(row.movie_idx))

    return dict(relevant_items_by_user)


def recommend_for_user(
    model: torch.nn.Module,
    user_idx: int,
    movie_indices: list[int],
    k: int,
) -> list[int]:
    model.eval()

    user_tensor = torch.tensor([user_idx] * len(movie_indices), dtype=torch.long)
    movie_tensor = torch.tensor(movie_indices, dtype=torch.long)

    with torch.no_grad():
        predictions = model(user_tensor, movie_tensor).tolist()

    ranked_items = sorted(
        zip(movie_indices, predictions),
        key=lambda item: item[1],
        reverse=True,
    )

    return [int(movie_idx) for movie_idx, _ in ranked_items[:k]]


def evaluate_ranking_metrics(
    model: torch.nn.Module,
    test_df: pd.DataFrame,
    num_movies: int,
    k: int = 10,
    relevance_threshold: float = 4.0,
) -> dict[str, float]:
    if k <= 0:
        raise ValueError("k must be greater than 0")

    relevant_items_by_user = build_relevant_items_by_user(
        test_df=test_df,
        relevance_threshold=relevance_threshold,
    )

    if not relevant_items_by_user:
        return {
            "precision_at_k": 0.0,
            "recall_at_k": 0.0,
            "ndcg_at_k": 0.0,
            "catalog_coverage": 0.0,
            "evaluated_users": 0.0,
        }

    movie_indices = list(range(num_movies))
    recommended_items_by_user: dict[int, list[int]] = {}

    precision_scores = []
    recall_scores = []
    ndcg_scores = []

    for user_idx, relevant_items in relevant_items_by_user.items():
        recommended_items = recommend_for_user(
            model=model,
            user_idx=user_idx,
            movie_indices=movie_indices,
            k=k,
        )

        recommended_items_by_user[user_idx] = recommended_items

        precision_scores.append(
            precision_at_k(
                recommended_items=recommended_items,
                relevant_items=relevant_items,
                k=k,
            )
        )
        recall_scores.append(
            recall_at_k(
                recommended_items=recommended_items,
                relevant_items=relevant_items,
                k=k,
            )
        )
        ndcg_scores.append(
            ndcg_at_k(
                recommended_items=recommended_items,
                relevant_items=relevant_items,
                k=k,
            )
        )

    catalog_items = set(movie_indices)

    return {
        "precision_at_k": round(sum(precision_scores) / len(precision_scores), 4),
        "recall_at_k": round(sum(recall_scores) / len(recall_scores), 4),
        "ndcg_at_k": round(sum(ndcg_scores) / len(ndcg_scores), 4),
        "catalog_coverage": round(
            catalog_coverage(
                recommended_items_by_user=recommended_items_by_user,
                catalog_items=catalog_items,
            ),
            4,
        ),
        "evaluated_users": float(len(relevant_items_by_user)),
    }