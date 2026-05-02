# Risk Register

## Purpose

This file tracks key project risks.

| Risk | Impact | Mitigation |
|---|---|---|
| Wrong model run ID | Inference startup failure | Validate `/ready` and Compose config |
| Checksum mismatch | Model fails to load | Keep approved SHA256 in promotion record |
| Missing MinIO bucket | Training artifact upload fails | Confirm `mlflow-artifacts` bucket |
| API key exposure | Unauthorized use | Do not commit `.env` |
| Open metrics endpoint | Operational detail exposure | Restrict in production |
| Weak local auth | Not production ready | Replace with JWT or gateway auth |
| Model quality gap | Poor recommendations | Add ranking metrics |
| Dataset drift | Training inconsistency | Add dataset checksum |
| Artifact mismatch | Bad serving state | Add artifact manifest |
| Docker cache confusion | Old image behavior | Rebuild inference and check logs |