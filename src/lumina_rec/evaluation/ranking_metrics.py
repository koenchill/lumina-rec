import math


def precision_at_k(recommended_items: list[int], relevant_items: set[int], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be greater than 0")

    if not recommended_items:
        return 0.0

    top_k = recommended_items[:k]
    hits = sum(1 for item in top_k if item in relevant_items)

    return hits / k


def recall_at_k(recommended_items: list[int], relevant_items: set[int], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be greater than 0")

    if not relevant_items:
        return 0.0

    top_k = recommended_items[:k]
    hits = sum(1 for item in top_k if item in relevant_items)

    return hits / len(relevant_items)


def dcg_at_k(recommended_items: list[int], relevant_items: set[int], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be greater than 0")

    score = 0.0

    for index, item in enumerate(recommended_items[:k]):
        if item in relevant_items:
            rank = index + 1
            score += 1.0 / math.log2(rank + 1)

    return score


def ndcg_at_k(recommended_items: list[int], relevant_items: set[int], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be greater than 0")

    if not relevant_items:
        return 0.0

    actual_dcg = dcg_at_k(recommended_items, relevant_items, k)
    ideal_hits = min(len(relevant_items), k)
    ideal_dcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))

    if ideal_dcg == 0:
        return 0.0

    return actual_dcg / ideal_dcg


def catalog_coverage(recommended_items_by_user: dict[int, list[int]], catalog_items: set[int]) -> float:
    if not catalog_items:
        return 0.0

    recommended_items = set()

    for items in recommended_items_by_user.values():
        recommended_items.update(items)

    return len(recommended_items) / len(catalog_items)