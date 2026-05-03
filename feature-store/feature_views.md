# Feature Views

## Purpose

This file defines planned feature views for a future Feast implementation.

## user_features

| Feature | Type | Description |
|---|---|---|
| user_id | integer | User identifier |
| rating_count | integer | Number of ratings by user |
| average_rating | float | Average user rating |

## movie_features

| Feature | Type | Description |
|---|---|---|
| movie_id | integer | Movie identifier |
| title | string | Movie title |
| genres | string | Movie genres |
| rating_count | integer | Number of ratings received |
| average_rating | float | Average movie rating |
| popularity_score | float | Future normalized popularity score |

## interaction_features

| Feature | Type | Description |
|---|---|---|
| user_id | integer | User identifier |
| movie_id | integer | Movie identifier |
| rating | float | User rating |
| timestamp | integer | Rating timestamp |