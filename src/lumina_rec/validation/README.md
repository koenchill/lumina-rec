# Model and Dataset Validation

## Purpose

This folder stores future validation utilities for Lumina Rec.

## Planned Checks

| Check | Purpose |
|---|---|
| Dataset schema check | Confirm required columns exist |
| Rating range check | Confirm ratings stay in expected range |
| Movie ID alignment check | Confirm ratings reference known movies |
| Dataset checksum check | Confirm training data integrity |
| Artifact manifest check | Confirm artifacts belong together |
| Model performance check | Confirm candidate meets baseline |

## Current Dataset

MovieLens latest small.

## Current Required Files

| File | Purpose |
|---|---|
| ratings.csv | User movie ratings |
| movies.csv | Movie title and genre metadata |