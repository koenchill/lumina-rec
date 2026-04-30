# Recommendation API

## Purpose

The recommendation API returns predicted MovieLens ratings and top N movie recommendations for a known user.

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /predict | Predicts a rating for one user and one movie |
| POST | /recommend | Returns top N recommendations for one user |

## Authentication

Both endpoints require:

```text
x-api-key: local-dev-api-key