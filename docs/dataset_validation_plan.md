# Dataset Validation Plan

## Purpose

This document defines dataset validation checks for Lumina Rec.

## Dataset

MovieLens latest small.

## Current Dataset Files

| File | Purpose |
|---|---|
| ratings.csv | User movie ratings |
| movies.csv | Movie metadata |

## Required Checks

| Check | Purpose |
|---|---|
| ratings file exists | Confirm training data is present |
| movies file exists | Confirm metadata is present |
| required columns exist | Prevent schema drift |
| no missing userId | Protect user mapping |
| no missing movieId | Protect movie mapping |
| no missing rating | Protect training target |
| rating range valid | Confirm ratings are within expected range |
| movie IDs align | Confirm ratings reference known movies |
| dataset checksum recorded | Confirm dataset integrity |

## Expected Columns

### ratings.csv

```text
userId
movieId
rating
timestamp