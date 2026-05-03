# Security Review Checklist

## Purpose

This checklist supports security review for Lumina Rec.

## Review Items

| Area | Question | Status |
|---|---|---|
| Authentication | Are protected endpoints using API key? |  |
| Authorization | Is future RBAC documented? |  |
| Secrets | Is `.env` excluded from Git? |  |
| Input validation | Are request models validated? |  |
| Rate limiting | Are protected endpoints rate limited? |  |
| Model integrity | Is SHA256 validation enabled? |  |
| Logging | Are logs structured and free of secrets? |  |
| Metrics | Is metrics exposure documented? |  |
| Container security | Is Trivy scanning planned or present? |  |
| Dependency risk | Is dependency management documented? |  |

## Review Outcome

| Decision | Notes |
|---|---|
| Accepted for local development |  |
| Needs remediation |  |