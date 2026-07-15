# Audit Logging Plan

## Purpose

This document defines future audit logging needs for Lumina Rec.

## Current Logs

The inference service writes structured JSON logs.

## Current Logged Events

| Event | Purpose |
|---|---|
| model_loaded | Model startup event |
| prediction_completed | Successful prediction |
| prediction_failed | Failed prediction |
| recommendation_completed | Successful recommendation |
| recommendation_failed | Failed recommendation |
| authentication_failed | Missing or invalid API key |
| rate_limit_exceeded | Rate limit event |
| model_checksum_failed | Model integrity failure |

## Future Audit Events

| Event | Purpose |
|---|---|
| model_promoted | Track model approval |
| model_rolled_back | Track rollback |
| registry_alias_changed | Track approved alias changes |
| dataset_validated | Track data validation |
| artifact_manifest_validated | Track artifact package validation |
| secret_rotated | Track credential hygiene |

## Audit Log Requirements

- Include timestamp.
- Include event name.
- Include request ID when available.
- Include model run ID when relevant.
- Do not log secrets.
- Do not log API keys.
- Preserve logs for review in production.