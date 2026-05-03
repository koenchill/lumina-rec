# Feature Store Entities

## Purpose

This file defines planned Feast entities.

## Entities

| Entity | Join Key | Description |
|---|---|---|
| user | user_id | MovieLens user |
| movie | movie_id | MovieLens movie |

## Planned Entity Use

| Entity | Used By |
|---|---|
| user | user_features, interaction_features, recommendations |
| movie | movie_features, interaction_features, recommendations |