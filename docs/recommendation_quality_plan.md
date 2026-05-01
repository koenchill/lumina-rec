# Recommendation Quality Plan

## Purpose

This document defines how Lumina Rec should evaluate recommendation quality.

## Current Model Metric

| Metric | Value |
|---|---|
| Test RMSE | 2.0162 |

## Current Limitation

The current model uses RMSE to evaluate rating prediction quality.

RMSE is useful for predicted rating accuracy, but it does not fully measure recommendation ranking quality.

## Future Quality Metrics

| Metric | Purpose |
|---|---|
| Precision at K | Measures useful recommendations in top K |
| Recall at K | Measures how many relevant items appear |
| MAP at K | Measures ranking quality |
| NDCG at K | Measures ranking quality with position weighting |
| Coverage | Measures catalog spread |
| Diversity | Measures variety in recommendations |
| Novelty | Measures less obvious recommendations |

## Recommended Evaluation Flow

1. Split user rating history into train and test.
2. Train the candidate model.
3. Generate top N recommendations.
4. Compare recommendations to held out ratings.
5. Calculate ranking metrics.
6. Compare candidate to approved baseline.
7. Promote only if metrics meet threshold.

## Future Promotion Gate

A model should not be promoted based on RMSE alone once ranking metrics are added.