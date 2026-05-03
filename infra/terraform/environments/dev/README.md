# Dev Environment

## Purpose

This folder will hold future Terraform configuration for the development environment.

## Planned Inputs

| Input | Purpose |
|---|---|
| environment_name | Environment label |
| region | Cloud region |
| inference_image | Container image URI |
| model_registry_name | Approved model registry name |
| model_alias | Approved model alias |
| api_domain | API DNS name |
| log_retention_days | Log retention policy |

## Planned Outputs

| Output | Purpose |
|---|---|
| inference_url | API endpoint |
| metrics_url | Internal metrics endpoint |
| artifact_bucket | Model artifact storage |
| registry_name | Model registry reference |

## Current Status

Placeholder only.