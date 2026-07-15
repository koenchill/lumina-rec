# Dependency Management

## Purpose

This document defines how Lumina Rec dependencies should be managed.

## Dependency Areas

| Area | File |
|---|---|
| Python project dependencies | pyproject.toml |
| Inference service dependencies | services/inference/requirements.txt |
| Docker base image | services/inference/Dockerfile |
| Local services | docker-compose.yml |

## Current Practices

- Pin inference dependencies.
- Use CPU only PyTorch for the inference image.
- Keep dependency files under version control.
- Use container scanning.
- Use secret scanning.

## Risks

| Risk | Impact |
|---|---|
| Unpinned dependencies | Reproducibility issues |
| Vulnerable package | Security exposure |
| Large image dependencies | Slow builds and larger attack surface |
| Version conflict | Build or runtime failure |

## Future Improvements

1. Add dependency audit to CI.
2. Add Dependabot.
3. Add SBOM generation.
4. Fail builds on critical dependency issues.
5. Review dependency updates before promotion.