# Zero Trust Alignment

## Purpose

This document explains how Lumina Rec aligns to Zero Trust principles.

## Current Alignment

| Principle | Current Implementation |
|---|---|
| Verify explicitly | `/predict` and `/recommend` require API key |
| Use least privilege | Local services are separated by Docker Compose service boundaries |
| Assume breach | Model checksum validation detects artifact mismatch |
| Continuous monitoring | Metrics and structured logs provide visibility |
| Strong configuration | Runtime values are documented and validated |
| Reduce implicit trust | Approved model artifacts are loaded by run ID and checksum |

## Current Gaps

| Gap | Future Control |
|---|---|
| Local API key only | Replace with JWT or API gateway authentication |
| Open metrics endpoint | Restrict metrics to internal network |
| Local `.env` secrets | Move to managed secret store |
| No production network controls | Add private subnets and security groups |
| No identity based authorization | Add RBAC or claims based authorization |

## Next Steps

1. Add JWT authentication.
2. Restrict metrics access.
3. Add managed secrets.
4. Add production network segmentation.
5. Add model registry alias based approval.