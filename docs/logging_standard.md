# Logging Standard

## Purpose

This document defines the logging standard for Lumina Rec.

## Current Logging Pattern

The inference service writes structured JSON logs.

## Current Events

| Event | Purpose |
|---|---|
| model_loaded | Approved model loaded |
| prediction_completed | Prediction succeeded |
| prediction_failed | Prediction failed |
| recommendation_completed | Recommendation succeeded |
| recommendation_failed | Recommendation failed |
| authentication_failed | API key missing or invalid |
| rate_limit_exceeded | Caller exceeded rate limit |
| model_checksum_failed | Model integrity validation failed |

## Required Log Fields

| Field | Purpose |
|---|---|
| event | Event name |
| request_id | Request trace ID |
| model_name | Served model name |
| model_version | Served model version |
| model_run_id | MLflow run ID |
| latency_ms | Request latency |
| status | success or error |
| error | Error details when available |

## Logging Rules

- Do not log API keys.
- Do not log secrets.
- Do not log `.env` values.
- Include request ID for prediction and recommendation events.
- Include model run ID for model serving events.
- Keep error messages useful but not sensitive.

## Future Improvements

- Add centralized log export.
- Add log redaction.
- Add correlation IDs across services.
- Add security event dashboard.