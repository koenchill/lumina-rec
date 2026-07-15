# API Security Plan

## Purpose

This document defines the API security plan for Lumina Rec.

## Current API Controls

| Control | Status |
|---|---|
| API key on `/predict` | Implemented |
| API key on `/recommend` | Implemented |
| Pydantic validation | Implemented |
| Unknown user rejection | Implemented |
| Unknown movie rejection | Implemented |
| Rate limiting | Implemented |
| Request ID | Implemented |
| Structured logging | Implemented |

## Current Protected Endpoints

| Endpoint | Protection |
|---|---|
| POST /predict | Requires `x-api-key` |
| POST /recommend | Requires `x-api-key` |

## Current Open Local Endpoints

| Endpoint | Reason |
|---|---|
| GET /health | Local service check |
| GET /ready | Local readiness check |
| GET /metrics | Local metrics check |

## Production Security Plan

| Area | Target Control |
|---|---|
| Authentication | JWT or API gateway |
| Authorization | Role based access control |
| Secrets | Managed secret store |
| Transport security | TLS |
| Metrics | Internal only |
| Rate limiting | Gateway level enforcement |
| Logging | Centralized and redacted |
| Abuse protection | Request limits and monitoring |

## Next Steps

1. Replace local API key with JWT.
2. Restrict `/metrics`.
3. Add gateway rate limiting.
4. Add auth failure alerting.
5. Add log redaction rules.