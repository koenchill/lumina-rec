# SBOM Plan

## Purpose

This document defines the future Software Bill of Materials plan for Lumina Rec.

## Current State

Lumina Rec has pinned Python dependencies and container scanning.

## SBOM Goals

| Goal | Purpose |
|---|---|
| Generate Python dependency SBOM | Track package inventory |
| Generate container image SBOM | Track image contents |
| Store SBOM as CI artifact | Support audit review |
| Review critical dependencies | Reduce supply chain risk |
| Compare SBOM across releases | Detect unexpected dependency changes |

## Candidate Tools

| Tool | Purpose |
|---|---|
| Syft | Generate SBOM |
| Trivy | Vulnerability scan and SBOM support |
| pip-audit | Python dependency vulnerability review |

## Future CI Steps

1. Build inference image.
2. Generate SBOM.
3. Run vulnerability scan.
4. Upload SBOM artifact.
5. Fail build on critical findings after policy is approved.