# Secrets Management Plan

## Purpose

This document defines the future secrets management approach for Lumina Rec.

## Current Local Pattern

Lumina Rec uses a local `.env` file.

This file must not be committed.

## Current Secrets and Sensitive Values

| Value | Purpose |
|---|---|
| AWS_ACCESS_KEY_ID | MinIO access key |
| AWS_SECRET_ACCESS_KEY | MinIO secret key |
| LUMINA_API_KEY | Local API key |
| MODEL_RUN_ID | Approved model selector |
| MODEL_SHA256 | Approved model checksum |

## Risks

| Risk | Impact |
|---|---|
| `.env` committed | Credential exposure |
| Shared local API key | Weak production access control |
| Long lived static secrets | Harder rotation |
| Manual secret updates | Human error |

## Target Production Pattern

| Area | Target |
|---|---|
| Secrets storage | Managed secret store |
| API authentication | JWT or API gateway |
| Service credentials | Short lived credentials where possible |
| Rotation | Documented rotation process |
| CI secrets | Repository or organization secret store |

## Safety Rules

- Do not commit `.env`.
- Do not paste secrets into issues or pull requests.
- Rotate secrets if exposed.
- Use `.env.example` for placeholders only.
- Use managed secrets for production.