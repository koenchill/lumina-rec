# API Assets

## Purpose

This folder stores API examples and API support documentation for Lumina Rec.

## Current Endpoints

| Endpoint | Purpose |
|---|---|
| GET /health | Service health |
| GET /ready | Model readiness |
| GET /metrics | Prometheus metrics |
| GET /movies/{movie_id} | Movie metadata lookup |
| POST /predict | Rating prediction |
| POST /recommend | Top N recommendations |

## Examples

| File | Purpose |
|---|---|
| examples/predict_request.json | Example `/predict` request |
| examples/recommend_request.json | Example `/recommend` request |
| examples/movie_response.json | Example `/movies/{movie_id}` response |
| examples/ready_response.json | Example `/ready` response |
| examples/recommend_response.json | Example `/recommend` response |