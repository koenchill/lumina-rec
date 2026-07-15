# Compliance Mapping

## Purpose

This document maps Lumina Rec controls to common security and governance themes.

## Control Mapping

| Area | Lumina Rec Control | Governance Value |
|---|---|---|
| Access control | API key required for protected endpoints | Reduces unauthorized use |
| Input validation | Pydantic request validation | Reduces malformed input risk |
| Model integrity | SHA256 model checksum validation | Reduces artifact tampering risk |
| Model governance | Approved artifact loading from MLflow | Improves model traceability |
| Logging | Structured JSON logs | Supports troubleshooting and audit review |
| Monitoring | Prometheus metrics endpoint | Supports operational visibility |
| Secrets | `.env` excluded from Git | Reduces credential exposure |
| Testing | Pytest API tests | Reduces regression risk |
| Load testing | Locust validation | Supports performance confidence |
| Rollback | Model rollback procedure | Supports recovery readiness |

## Future Compliance Enhancements

| Enhancement | Purpose |
|---|---|
| Managed secrets | Improve credential governance |
| Centralized logs | Improve audit evidence |
| Model registry alias | Improve model approval process |
| Artifact signing | Improve model supply chain assurance |
| Dataset checksum | Improve training data integrity |