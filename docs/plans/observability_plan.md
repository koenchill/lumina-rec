# Observability Plan

## Purpose

This document defines the observability plan for Lumina Rec.

## Current Observability

Lumina Rec currently supports:

| Capability | Location |
|---|---|
| Health check | `/health` |
| Readiness check | `/ready` |
| Prometheus metrics | `/metrics` |
| Structured logs | Inference container logs |
| Request IDs | Prediction and recommendation responses |
| Latency tracking | Response metadata and Prometheus histogram |

## Current Metrics

```text
lumina_prediction_requests_total
lumina_prediction_errors_total
lumina_prediction_latency_ms
lumina_rate_limit_errors_total