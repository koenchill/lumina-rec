# Lumina Rec Inference API Threat Model

## Scope

This threat model covers the local FastAPI inference service for Lumina Rec.

The service exposes:

- GET /health
- GET /ready
- GET /metrics
- POST /predict

## Assets

| Asset | Why It Matters |
|---|---|
| Model artifact | Drives predictions and must not be tampered with |
| Prediction API | Public facing service in future deployment |
| Request data | Could contain sensitive user or behavioral signals later |
| Metrics endpoint | Could expose operational details |
| Logs | Could contain request metadata and errors |
| MLflow artifacts | Stores model files and experiment outputs |
| MinIO credentials | Control artifact storage access |

## Trust Boundaries

| Boundary | Description |
|---|---|
| Client to API | External request enters the inference service |
| API to model file | Service loads model artifact from local path |
| API to logs | Request metadata is written to logs |
| API to metrics | Runtime metrics are exposed to monitoring |
| Training to MLflow | Training code logs model artifacts and metadata |
| MLflow to MinIO | MLflow writes artifacts to object storage |

## Main Threats

| Threat | Risk | Current Control | Next Control |
|---|---|---|---|
| Invalid input payload | API errors or unexpected behavior | Pydantic validation | Add stricter schema and bounds |
| Model artifact tampering | Bad predictions or malicious model behavior | Local file path only | Add checksum validation |
| Unauthenticated prediction access | Anyone could call the API | None yet | Add API key or JWT auth |
| Metrics exposure | Operational details could leak | Local only | Restrict metrics endpoint |
| Secret leakage | MinIO or MLflow credentials could be exposed | .env ignored by Git | Add secret scanning |
| Log leakage | Sensitive inputs could end up in logs | Logs avoid full payload | Add log redaction policy |
| Dependency risk | Vulnerable packages could enter image | Manual dependency install | Add dependency scanning |
| Container risk | Image may include vulnerable packages | Slim Python base | Add image scanning |
| Denial of service | High request volume could overwhelm API | Load tested with 10 users | Add rate limiting |
| Model drift | Prediction quality could degrade | Not implemented | Add monitoring and drift checks |

## Current Security Controls

- Input validation through Pydantic.
- Health and readiness endpoints.
- Structured logs with request IDs.
- Prometheus style metrics.
- Dockerized inference service.
- `.env` excluded from Git.
- Local load testing completed.
- CI runs tests and container health checks.

## Security Gaps

- No authentication on `/predict`.
- No authorization model.
- No rate limiting.
- No model artifact checksum.
- No secret scanner in CI.
- No container vulnerability scanner.
- No TLS in local setup.
- No production network segmentation yet.

## Recommended Next Controls

1. Add API key authentication for `/predict`.
2. Add request rate limiting.
3. Add model artifact checksum verification.
4. Add GitHub secret scanning or Gitleaks.
5. Add Docker image vulnerability scan with Trivy.
6. Restrict `/metrics` to internal network in production.
7. Add structured error handling without leaking internals.
8. Add audit logging for prediction requests.
9. Add model version promotion policy.
10. Add rollback plan for bad model deployments.

## Abuse Cases

### Abuse Case 1, Invalid Payload Flood

An attacker sends malformed requests repeatedly.

Expected control:

- Pydantic rejects invalid payloads.
- Rate limiting blocks excessive requests.
- Logs capture repeated failures.

### Abuse Case 2, Model Artifact Replacement

An attacker replaces the local model file.

Expected control:

- API checks model checksum at startup.
- CI records trusted artifact checksum.
- Deployment blocks unknown artifacts.

### Abuse Case 3, Metrics Scraping

An attacker scrapes `/metrics` for operational details.

Expected control:

- Metrics endpoint restricted to internal monitoring.
- External access blocked at gateway or firewall.

### Abuse Case 4, Credential Leak

A developer commits `.env`.

Expected control:

- `.gitignore` excludes `.env`.
- Secret scanner blocks commit or PR.
- Credentials are rotated if exposed.

## Security Acceptance Criteria

The inference API is ready for the next maturity stage when:

- `/predict` requires authentication.
- Invalid requests return controlled errors.
- Secrets are not committed.
- CI checks tests and image build.
- Metrics are available for monitoring.
- Logs include request IDs.
- The model artifact has integrity checks.
- Load test passes with zero failures.