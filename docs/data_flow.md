# Data Flow

## Purpose

This file explains how data moves through Lumina Rec.

## Training Data Flow

1. Training script downloads MovieLens data.
2. Ratings and movie metadata are loaded.
3. User IDs and movie IDs are encoded into model indices.
4. Matrix factorization model is trained.
5. Model metrics are calculated.
6. Artifacts are written locally.
7. Artifacts are logged to MLflow.
8. MLflow stores artifacts in MinIO.
9. MLflow stores metadata in Postgres.

## Inference Data Flow

1. Client sends request to FastAPI.
2. API validates payload.
3. API checks API key for protected endpoints.
4. API loads mappings and model artifacts from MLflow.
5. API validates model checksum.
6. API maps user and movie IDs to model indices.
7. Model returns predicted rating.
8. API returns response with model metadata and request ID.

## Recommendation Data Flow

1. Client sends `user_id` and `top_n`.
2. API validates user ID and top N.
3. API scores candidate movies for the user.
4. API sorts movies by predicted rating.
5. API returns top N recommendations.
6. Recommendation response includes movie metadata when available.