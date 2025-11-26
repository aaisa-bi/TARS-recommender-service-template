from __future__ import annotations

from hashlib import sha256
from typing import Annotated

from fastapi import Header, HTTPException, status
from loguru import logger

from settings import settings

ApiKeyHeader = Annotated[str | None, Header(convert_underscores=True)]


def _compute_hash(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def api_key_dependency(api_key: ApiKeyHeader = None) -> None:
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    expected_hash = (
        settings.api_key_hash.get_secret_value() if settings.api_key_hash else None
    )
    if not expected_hash:
        logger.warning("API key hash not configured.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key not configured",
        )

    if _compute_hash(api_key) != expected_hash:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
