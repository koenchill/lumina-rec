# Model Registry Module

## Purpose

Stores logical model registry metadata in Kubernetes for the approved serving pin.

## Responsibilities

- Create `model-registry-config` ConfigMap
- Hold registered model name, alias, artifact path, and registry-enable flag

## Current status

Implemented as local metadata ConfigMap. Full cloud registry resources are future work.
