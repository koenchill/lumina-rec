from fastapi import HTTPException

from services.inference.app.config import API_KEY
from services.inference.app.logging_utils import log_event


def raise_api_error(
    status_code: int,
    error_code: str,
    detail: str,
    request_id: str | None = None,
) -> None:
    raise HTTPException(
        status_code=status_code,
        detail={
            "error_code": error_code,
            "detail": detail,
            "request_id": request_id,
        },
    )


def verify_api_key(
    x_api_key: str | None,
    request_id: str | None = None,
) -> None:
    if not x_api_key or x_api_key != API_KEY:
        log_event(
            "authentication_failed",
            request_id=request_id,
            status="error",
        )
        raise_api_error(
            status_code=401,
            error_code="AUTH_INVALID_API_KEY",
            detail="Invalid or missing API key",
            request_id=request_id,
        )
