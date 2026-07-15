# Movie Metadata Enrichment Plan

## Purpose

This document defines the plan to add movie title and genre metadata to Lumina Rec responses.

## Current State

The `/recommend` endpoint returns:

- movie_id
- predicted_rating

## Target State

The `/recommend` endpoint should return:

- movie_id
- title
- genres
- predicted_rating

## Available Artifact

The training workflow already logs:

```text
movies_metadata.csv