# Lumina Rec Security Controls

## Purpose

This document maps the security controls implemented in Lumina Rec to practical risk reduction outcomes.

The current system is a local MLOps inference stack that trains and serves a MovieLens matrix factorization recommender. It is not production hosted yet, but it uses production style security patterns.

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| Dataset | MovieLens latest small |
| Model type | Matrix factorization |
| MLflow run ID | 248c55bf41994c05923a86e354158303 |
| Artifact path | approved_model |
| Model SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 |
| Test RMSE | 2.0423 |

## Implemented Controls

| Control Area | Implemented Control | Risk Reduced |
|---|---|---|
| API authentication | `/predict` requires `x-api-key` | Reduces unauthorized inference access |
| Input validation | Pydantic requires `user_id` and `movie_id` | Reduces malformed request risk |
| Unknown entity handling | Unknown users and movies return 404 | Prevents unsupported predictions from unknown mappings |
| Health checks | `/health` endpoint | Confirms API process is alive |
| Readiness checks | `/ready` confirms approved model load status | Reduces failed traffic routing to unready service |
| Approved model loading | Inference loads artifacts from MLflow by `MODEL_RUN_ID` | Reduces risk of serving an unapproved local model |
| Model checksum validation | SHA256 validates the downloaded model artifact | Reduces model tampering and artifact corruption risk |
| Structured logging | Prediction events include request ID, model name, model version, MLflow run ID, latency, and status | Improves debugging and incident response |
| Metrics | `/metrics` exposes request count, error count, latency, and rate limit errors | Supports monitoring and service reliability |
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
| Experiment tracking | MLflow records model runs, parameters, metrics, and artifacts | Improves model traceability |

## Security Outcomes

The current implementation improves security in six areas.

### 1. Access Control

The prediction endpoint is no longer open. A caller must provide the expected API key.

### 2. Model Governance

The inference service loads the approved MovieLens model artifact from MLflow by run ID. The model is not treated as an untracked local file.

### 3. Model Integrity

The model artifact must match the approved SHA256 hash before the service becomes ready.

### 4. Reliability

Health checks, readiness checks, tests, and load testing provide early warning when the service breaks.

### 5. Observability

Structured logs and Prometheus metrics provide operational visibility.

### 6. Supply Chain Awareness

Gitleaks and Trivy add checks for secrets and container vulnerabilities.

## Current Gaps

| Gap | Risk | Planned Control |
|---|---|---|
| API key is local development only | Weak authentication for real deployment | Replace with JWT or managed API gateway auth |
| Metrics endpoint is open locally | Could expose operational details | Restrict metrics to internal network |
| No production rate limit enforcement layer | App level rate limiting may not be enough | Add gateway or ingress rate limiting |
| No TLS locally | Traffic is not encrypted | Terminate TLS at gateway or ingress in production |
| No role based authorization | All valid API callers have same access | Add RBAC through identity provider |
| No formal secret manager | Local `.env` is acceptable only for development | Use AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager |
| Trivy is report only | Vulnerabilities do not fail CI yet | Change Trivy exit code to fail on critical findings |
| Dependency pinning still needs final validation | Dependency drift could break builds | Pin inference requirements and validate Docker build |
| No production network segmentation | Services share local network | Use VPC, private subnets, security groups, and least privilege IAM |
| Model performance is baseline only | RMSE is not optimized yet | Improve training, tuning, and evaluation workflow |

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
| MovieLens training | completed |
| MLflow run ID | 248c55bf41994c05923a86e354158303 |
| Model SHA256 | c276920f586da4cf246c20e1b5b4142f022fae1f7c402dd725475712bf1374b6 |
| Test RMSE | 2.0423 |
| Readiness check | passed |
| Prediction check | passed |
| Prediction response | returned `predicted_rating`, `user_id`, `movie_id`, model metadata, request ID, and latency |
| Previous load test requests | 446 |
| Previous load test failures | 0 |
| Previous failure rate | 0.00% |

## Next Security Improvements

1. Add a top N recommendation endpoint with controlled output size.
2. Add movie title metadata to prediction responses.
3. Refresh Locust baseline after the MovieLens transition.
4. Replace local API key with JWT or gateway based authentication.
5. Restrict `/metrics` to internal monitoring.
6. Enforce Trivy failure on critical vulnerabilities.
7. Finalize dependency pinning and vulnerability review.
8. Add production deployment network design.
9. Add incident response evidence collection.
10. Add model promotion and rollback approval workflow.