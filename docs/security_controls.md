# Lumina Rec Security Controls

## Purpose

This document maps the security controls implemented in Lumina Rec to practical risk reduction outcomes.

The current system is a local MLOps inference stack. It is not production hosted yet, but it uses production style security patterns.

## Implemented Controls

| Control Area | Implemented Control | Risk Reduced |
|---|---|---|
| API authentication | `/predict` requires `x-api-key` | Reduces unauthorized inference access |
| Input validation | Pydantic requires exactly 10 feature values | Reduces malformed request risk |
| Health checks | `/health` endpoint | Confirms API process is alive |
| Readiness checks | `/ready` endpoint confirms model load status | Reduces failed traffic routing to unready service |
| Structured logging | Prediction events include request ID, model name, model version, latency, and status | Improves debugging and incident response |
| Metrics | `/metrics` exposes request count, error count, and latency | Supports monitoring and service reliability |
| Automated tests | Pytest validates API behavior | Reduces regression risk |
| Load testing | Locust validates inference under repeated requests | Reduces performance uncertainty |
| Secret handling | `.env` excluded from Git | Reduces accidental credential exposure |
| Safe config template | `.env.example` documents local variables without committing private `.env` | Improves setup consistency |
| CI test gate | GitHub Actions runs inference API tests | Blocks broken API changes |
| CI Docker build | GitHub Actions builds the inference image | Confirms deployable container build |
| CI container startup check | GitHub Actions starts container and checks health, readiness, metrics, and prediction | Confirms runtime behavior |
| Secret scanning | Gitleaks scans repository history and commits | Reduces leaked secret risk |
| Container scanning | Trivy scans the inference image | Improves visibility into OS and library vulnerabilities |
| Artifact storage | MLflow artifacts stored in MinIO | Separates model artifact storage from code |
| Experiment tracking | MLflow records model runs and metadata | Improves model traceability |

## Security Outcomes

The current implementation improves security in five areas:

1. Access control

The prediction endpoint is no longer open. A caller must provide the expected API key.

2. Reliability

Health, readiness, tests, and load testing give early warning when the service breaks.

3. Observability

Structured logs and Prometheus metrics provide operational visibility.

4. Supply chain awareness

Gitleaks and Trivy add checks for secrets and container vulnerabilities.

5. Model governance foundation

MLflow tracks model runs, parameters, and artifacts, which supports future promotion and rollback workflows.

## Current Gaps

| Gap | Risk | Planned Control |
|---|---|---|
| API key is local development only | Weak authentication for real deployment | Replace with JWT or managed API gateway auth |
| Metrics endpoint is open locally | Could expose operational details | Restrict metrics to internal network |
| No rate limiting | API could be abused under high request volume | Add rate limiting middleware or gateway control |
| No TLS locally | Traffic is not encrypted | Terminate TLS at gateway or ingress in production |
| No model checksum validation | Model artifact tampering may go undetected | Add startup checksum verification |
| No role based authorization | All valid API callers have same access | Add RBAC through identity provider |
| No formal secret manager | Local `.env` is acceptable only for development | Use AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager |
| Trivy is report only | Vulnerabilities do not fail CI yet | Change Trivy exit code to fail on critical findings |
| No dependency pinning strategy finalized | Dependency drift could break builds | Pin versions in lock file and CI |
| No production network segmentation | Services share local network | Use VPC, private subnets, security groups, and least privilege IAM |

## CI Security Gates

The CI pipeline currently validates:

- Secret scanning with Gitleaks
- Inference API tests
- Docker image build
- Trivy vulnerability scan
- Container startup
- Health endpoint
- Readiness endpoint
- Metrics endpoint
- Authenticated prediction request

## Evidence

Local validation confirmed:

| Test | Result |
|---|---|
| Inference API tests | 7 passed |
| Load test requests | 446 |
| Load test failures | 0 |
| Failure rate | 0.00% |
| Predict median latency | 48 ms |
| Predict p95 latency | 51 ms |

## Next Security Improvements

1. Add rate limiting to `/predict`.
2. Add model artifact checksum validation.
3. Replace local API key with JWT or gateway based authentication.
4. Restrict `/metrics` to internal monitoring.
5. Enforce Trivy failure on critical vulnerabilities.
6. Add dependency pinning and vulnerability review.
7. Add production deployment network design.
8. Add incident response runbook.
9. Add model rollback procedure.
10. Add audit logging policy.