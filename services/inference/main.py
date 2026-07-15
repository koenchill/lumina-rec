"""Compatibility entrypoint for uvicorn and tests.

Prefer: `services.inference.app.main:app`
"""

from services.inference.app.main import app

__all__ = ["app"]
