# Lumina Rec Deployment Notes

## Purpose

This document captures deployment decisions for the local Lumina Rec MLOps stack.

## Inference Container

The inference image uses `python:3.11-slim`.

The container installs the CPU only PyTorch wheel from:

```text
https://download.pytorch.org/whl/cpu