# Data Governance Plan

## Purpose

This document defines data governance expectations for Lumina Rec.

## Current Dataset

MovieLens latest small.

## Current Data Types

| Data | Description |
|---|---|
| ratings.csv | User movie ratings |
| movies.csv | Movie titles and genres |
| derived mappings | User and movie ID index mappings |
| model artifacts | Trained model and metadata |

## Governance Rules

| Rule | Purpose |
|---|---|
| Keep raw data separate | Preserve source integrity |
| Keep processed data separate | Support reproducibility |
| Track dataset source | Support lineage |
| Validate schema | Prevent training failures |
| Validate rating range | Protect model quality |
| Validate movie references | Prevent mapping errors |
| Record dataset checksum | Support integrity review |

## Current Gaps

| Gap | Future Control |
|---|---|
| No dataset checksum yet | Add checksum validation |
| No formal data card yet | Add dataset card |
| No automated data quality gate yet | Add validation to training |
| No drift monitoring yet | Add production monitoring later |