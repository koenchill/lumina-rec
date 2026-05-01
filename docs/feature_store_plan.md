# Feature Store Plan

## Purpose

This document defines the future feature store plan for Lumina Rec.

## Current State

Lumina Rec currently uses local MovieLens mappings and metadata loaded from MLflow artifacts.

## Target State

Use a feature store to manage reusable user, movie, and interaction features.

## Candidate Tool

Feast.

## Candidate Feature Groups

| Feature Group | Example Features |
|---|---|
| user_features | user_id, rating_count, average_rating |
| movie_features | movie_id, genre_count, average_rating, popularity_score |
| interaction_features | user_id, movie_id, rating, timestamp |
| recommendation_features | predicted_rating, rank, model_version |

## Benefits

- Consistent training and inference features
- Better feature reuse
- Clear feature ownership
- Easier feature validation
- Better path toward production MLOps

## Future Tasks

1. Define Feast repository structure.
2. Create user feature views.
3. Create movie feature views.
4. Create interaction feature views.
5. Add offline feature generation.
6. Add online feature serving pattern.
7. Add feature validation tests.