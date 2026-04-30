# Testing Strategy

## Purpose

This document explains how Lumina Rec validates the local MLOps stack.

## Test Types

| Test Type | Tool | Purpose |
|---|---|---|
| API tests | Pytest | Validate endpoint behavior |
| Load tests | Locust | Validate repeated API requests |
| Health checks | PowerShell runner | Confirm service availability |
| Readiness checks | PowerShell runner | Confirm approved model loaded |
| CI checks | GitHub Actions | Validate code, container, and security checks |

## API Test Coverage

The test suite validates:

- Health endpoint
- Readiness endpoint
- Prediction endpoint
- Missing API key rejection
- Invalid API key rejection
- Missing required fields
- Unknown user handling
- Unknown movie handling
- Metrics endpoint

## Load Test Coverage

The Locust test validates:

- GET /health
- POST /predict
- Required response fields
- Zero failure baseline

## Commands

```powershell
.\scripts\lumina.ps1 test
.\scripts\lumina.ps1 load-test