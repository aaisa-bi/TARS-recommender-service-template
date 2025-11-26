import importlib
import os

import pytest
from fastapi import HTTPException

import settings
from app.utils import auth


def test_api_key_dependency_without_hash(monkeypatch: pytest.MonkeyPatch) -> None:
    os.environ.pop("API_KEY_HASH", None)
    importlib.reload(settings)
    importlib.reload(auth)
    settings.api_key_hash = None
    auth.settings = settings

    with pytest.raises(HTTPException) as excinfo:
        auth.api_key_dependency("any-key")

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "API key not configured"
