from __future__ import annotations

import importlib
import os
from hashlib import sha256
from typing import Callable, Optional

import pytest
from fastapi.testclient import TestClient


def _build_client(
    monkeypatch: pytest.MonkeyPatch,
    api_key: Optional[str],
    load_art_override: Optional[Callable[[], str]] = None,
) -> TestClient:
    os.environ["ENV"] = "test"
    if api_key:
        os.environ["API_KEY_HASH"] = sha256(api_key.encode("utf-8")).hexdigest()
    else:
        os.environ.pop("API_KEY_HASH", None)

    import settings

    importlib.reload(settings)

    import app.utils.auth as auth
    importlib.reload(auth)
    if api_key is None:
        settings.api_key_hash = None
        auth.settings = settings

    import app.utils.art as art
    importlib.reload(art)
    if load_art_override:
        monkeypatch.setattr(art, "load_ascii_art", load_art_override)

    import app.model.recommender as recommender
    importlib.reload(recommender)

    import app.main as main
    importlib.reload(main)

    return TestClient(main.app)


@pytest.fixture()
def api_key() -> str:
    return "test-key"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch, api_key: str) -> TestClient:
    return _build_client(monkeypatch, api_key)


def test_recommend_action_success(client: TestClient, api_key: str) -> None:
    payload = {
        "id": "evt-1",
        "event_metadata": {"foo": "bar"},
        "user_metadata": {"user": "abc"},
    }

    response = client.post(
        "/recommend-action",
        headers={"api-key": api_key},
        json=payload,
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "action_channel": "web",
            "action_metadata": {"message": "hello client"},
        }
    ]


def test_missing_api_key(client: TestClient) -> None:
    payload = {"id": "evt-2", "event_metadata": {}, "user_metadata": {}}

    response = client.post("/recommend-action", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing API key"


def test_invalid_api_key(client: TestClient) -> None:
    payload = {"id": "evt-3", "event_metadata": {}, "user_metadata": {}}

    response = client.post(
        "/recommend-action",
        headers={"api-key": "wrong-key"},
        json=payload,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API key"


def test_invalid_event_payload(client: TestClient, api_key: str) -> None:
    payload = {"event_metadata": {}, "user_metadata": {}}

    response = client.post(
        "/recommend-action",
        headers={"api-key": api_key},
        json=payload,
    )

    assert response.status_code == 422


def test_api_key_not_configured(monkeypatch: pytest.MonkeyPatch, api_key: str) -> None:
    client = _build_client(monkeypatch, api_key=None)
    response = client.post(
        "/recommend-action",
        headers={"api-key": api_key},
        json={"id": "evt-4", "event_metadata": {}, "user_metadata": {}},
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "API key not configured"


def test_lifespan_logs_banner(monkeypatch: pytest.MonkeyPatch, api_key: str) -> None:
    calls: list[str] = []

    def fake_load_art() -> str:
        calls.append("banner-called")
        return "BANNER"

    client = _build_client(monkeypatch, api_key=api_key, load_art_override=fake_load_art)
    with client:
        pass

    assert calls == ["banner-called"]
