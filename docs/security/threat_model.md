# Lumina Rec Inference API Threat Model

## Scope

This threat model covers the local Lumina Rec inference API and supporting MLOps workflow.

The current service trains and serves a MovieLens matrix factorization recommender.

The service exposes:

- GET /health
- GET /ready
- GET /metrics
- POST /predict
- POST /recommend

## Current Approved Model

| Field | Value |
|---|---|
| Model name | lumina-rec-movielens-mf |
| Model version | 0.2.0 |
| Dataset | MovieLens latest small |
| Model type | Matrix factorization |
| MLflow run ID | 14eda4cf03bd4d328a3ee791ec9a002f |
| Artifact path | approved_model |
| Model SHA256 | 205de2403fdd84e1826dbde3e2f52470e36198d7c4f4953a5e0118e3040b14cd |
| Test RMSE | 2.0162 |

## Assets

| Asset | Why It Matters |
|---|---|
| Approved MLflow model artifact | Drives predictions and recommendations |
| Model SHA256 | Confirms the model artifact has not changed unexpectedly |
| MovieLens mappings | Maps user and movie IDs to model indices |
| Prediction API | Serves predicted ratings |
| Recommendation API | Serves top N movie recommendations |
| Request data | Contains user IDs, movie IDs, and requested recommendation size |
| Metrics endpoint | Exposes operational performance details |
| Logs | Contain request IDs, model metadata, and error events |
| MLflow metadata | Tracks runs, parameters, metrics, and artifact paths |
| MinIO artifact storage | Stores approved model artifacts |
| Postgres metadata store | Stores MLflow backend metadata |
| Local secrets | Control access to MinIO, MLflow artifacts, and API calls |

## Trust Boundaries

| Boundary | Description |
|---|---|
| Client to API | External request enters the inference service |
| API to authentication check | `/predict` and `/recommend` require `x-api-key` |
| API to MLflow | Inference service requests approved artifacts by `MODEL_RUN_ID` |
| MLflow to MinIO | MLflow retrieves model artifacts from object storage |
| API to model artifact | Service loads the downloaded model artifact |
| API to checksum validation | Service verifies SHA256 before serving traffic |
| API to logs | Request metadata and errors are written to logs |
| API to metrics | Runtime metrics are exposed for monitoring |
| Training to MLflow | Training logs metrics, parameters, and approved artifacts |

## Main Threats

| Threat | Risk | Current Control | Next Control |
|---|---|---|---|
| Invalid request payload | API errors or unsupported prediction requests | Pydantic validation | Add stricter schema constraints |
| Unknown user or movie ID | Model receives unsupported mapping values | API returns 404 for unknown IDs | Add clear client guidance and dataset metadata endpoint |
| Excessive recommendation size | Large responses or increased inference load | `top_n` limited to 1 through 50 | Add gateway level request limits |
| Unauthenticated prediction access | Anyone could call `/predict` | API key required | Replace local API key with JWT or gateway auth |
| Unauthenticated recommendation access | Anyone could call `/recommend` | API key required | Replace local API key with JWT or gateway auth |
| Model artifact tampering | Bad or malicious predictions | SHA256 validation before readiness | Add signed model artifacts |
| Unapproved model serving | API serves a local or wrong model file | Loads artifacts by `MODEL_RUN_ID` from MLflow | Add model registry promotion stage |
| Artifact storage credential leak | Unauthorized artifact access | `.env` excluded from Git | Use managed secret store |
| Metrics exposure | Operational details could leak | Local only | Restrict metrics endpoint in production |
| Log leakage | Logs could expose sensitive request metadata later | Logs avoid raw secrets | Add log redaction policy |
| Dependency risk | Vulnerable packages could enter image | Trivy scan in CI | Enforce failure on critical findings |
| Container risk | Image could include vulnerable OS or library packages | Python slim base and Trivy scan | Add hardened base image review |
| Denial of service | High traffic could overwhelm API | App level rate limiting | Add gateway or ingress rate limiting |
| Model drift | Prediction quality could degrade | MLflow tracks RMSE and run metadata | Add drift monitoring |
| Training data integrity issue | Bad dataset could degrade model quality | Dataset source is fixed for local demo | Add dataset checksum and data validation |
| Artifact mapping mismatch | Model and mappings could be out of sync | Artifacts logged together under `approved_model` | Add artifact manifest validation |

## Current Security Controls

- API key authentication required for `/predict`.
- API key authentication required for `/recommend`.
- Input validation through Pydantic.
- `top_n` limited to 1 through 50.
- Unknown `user_id` and `movie_id` return 404.
- Health and readiness endpoints.
- Readiness response includes model name, version, run ID, artifact path, SHA256, and checksum status.
- Approved model artifacts loaded from MLflow by `MODEL_RUN_ID`.
- Model checksum validation before the service becomes ready.
- Structured logs with request IDs and model metadata.
- Prometheus style metrics.
- Dockerized inference service.
- `.env` excluded from Git.
- Local load testing completed.
- CI runs tests and container health checks.
- Gitleaks secret scanning in CI.
- Trivy container vulnerability scanning in CI.

## Security Gaps

| Gap | Risk | Planned Control |
|---|---|---|
| API key is local development only | Weak production authentication | Replace with JWT or managed gateway authentication |
| No model registry stage gate | Approved model is identified by run ID only | Add MLflow Model Registry stage or alias |
| No signed model artifact | SHA256 proves integrity, but not signer identity | Add artifact signing |
| No dataset checksum | Training data integrity is not independently verified | Add dataset checksum validation |
| Metrics endpoint is open locally | Operational details could leak if exposed | Restrict metrics to internal monitoring |
| No TLS locally | Traffic is not encrypted | Terminate TLS at ingress or gateway |
| No RBAC | All valid callers share the same access | Add role based access control |
| No formal secret manager | `.env` is local only | Use AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager |
| Trivy is report only | Vulnerabilities do not fail CI yet | Fail CI on critical findings |
| No production network segmentation | Services share local network | Use private subnets, security groups, and least privilege IAM |
| Model performance is baseline only | RMSE is not optimized | Add model evaluation gates |

## Abuse Cases

## Abuse Case 1, Missing or Bad API Key

An attacker sends requests to `/predict` or `/recommend` without a valid API key.

Expected behavior:

- API returns 401.
- Logs capture `authentication_failed`.
- Metrics continue to report service health.

## Abuse Case 2, Unknown User or Movie

A caller sends a `user_id` or `movie_id` outside the approved MovieLens mappings.

Expected behavior:

- API returns 404.
- Model inference is not executed for unsupported IDs.
- Error count increases.

## Abuse Case 3, Excessive Recommendation Request

A caller requests too many recommendations.

Expected behavior:

- API returns 422 when `top_n` is above 50.
- Recommendation response size stays bounded.

## Abuse Case 4, Model Artifact Replacement

An attacker or bad process replaces the approved model artifact.

Expected behavior:

- SHA256 validation fails.
- Inference service fails startup.
- `/ready` does not pass.
- Logs show checksum validation failure.

## Abuse Case 5, Wrong MLflow Run ID

A bad deployment points `MODEL_RUN_ID` to the wrong run.

Expected behavior:

- If artifacts are missing, startup fails.
- If checksum does not match, startup fails.
- If checksum matches, `/ready` exposes the run ID for review.

## Abuse Case 6, Metrics Scraping

An attacker scrapes `/metrics` for operational details.

Expected behavior:

- Local setup allows metrics access.
- Production design should restrict metrics to internal monitoring only.

## Abuse Case 7, Credential Leak

A developer commits `.env`.

Expected behavior:

- `.gitignore` excludes `.env`.
- Gitleaks scans commits and repository history.
- Exposed credentials should be rotated.

## Security Acceptance Criteria

The inference API is ready for the next maturity stage when:

- `/predict` requires authentication.
- `/recommend` requires authentication.
- Invalid requests return controlled errors.
- Unknown users and movies return 404.
- `top_n` is bounded.
- Approved model artifacts load from MLflow.
- Model checksum validation is enabled.
- Secrets are not committed.
- CI checks tests and image build.
- Metrics are available for monitoring.
- Logs include request IDs.
- The model artifact has integrity checks.
- Load test passes with 0 failures.
- A model promotion and rollback procedure exists.

## Recommended Next Controls

1. Add MLflow Model Registry stage or alias for promotion.
2. Add signed artifact verification.
3. Add dataset checksum validation.
4. Add movie title and genre metadata to recommendation responses.
5. Add `/movies/{movie_id}` lookup endpoint.
6. Replace local API key with JWT or gateway authentication.
7. Restrict `/metrics` to internal monitoring.
8. Enforce Trivy failure on critical findings.
9. Add model performance acceptance gate before promotion.
10. Add recommendation quality evaluation.