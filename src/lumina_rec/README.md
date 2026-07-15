# lumina_rec

Shared Python library used by training jobs and the inference service.

| Package | Purpose |
|---|---|
| `lumina_rec.models` | Shared PyTorch matrix factorization model |
| `lumina_rec.evaluation` | Ranking metrics and evaluation helpers |
| `lumina_rec.registry` | MLflow Model Registry resolve/register helpers |
| `lumina_rec.validation` | Dataset checks and artifact manifest validation |

Install editable from the repo root (`uv sync` / `pip install -e .`) or set `PYTHONPATH=src`.
