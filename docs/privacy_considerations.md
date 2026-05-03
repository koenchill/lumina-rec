# Privacy Considerations

## Purpose

This document captures privacy considerations for Lumina Rec.

## Current Dataset

Lumina Rec uses the public MovieLens latest small dataset.

## Current API Inputs

| Field | Description |
|---|---|
| user_id | MovieLens user identifier |
| movie_id | MovieLens movie identifier |
| top_n | Number of recommendations requested |

## Current API Outputs

| Output | Description |
|---|---|
| predicted_rating | Predicted score |
| recommendations | Recommended movie IDs, titles, genres, and predicted ratings |
| request_id | Runtime trace identifier |
| latency_ms | Runtime performance metadata |

## Privacy Position

The current project is for local development and portfolio demonstration.

It does not use production customer data.

## Privacy Rules

- Do not add real customer data.
- Do not log API keys.
- Do not log secrets.
- Do not commit `.env`.
- Do not use sensitive datasets without a documented data handling plan.

## Future Production Considerations

- Data minimization.
- User consent and lawful basis if real users are involved.
- Retention policy.
- Access controls.
- Audit logging.
- Deidentification or pseudonymization where needed.