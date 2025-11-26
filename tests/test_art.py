from pathlib import Path

import pytest

from app.utils import art


def test_load_ascii_art_success() -> None:
    content = art.load_ascii_art()
    assert isinstance(content, str)
    assert content.strip() != ""


def test_load_ascii_art_failure(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.txt"
    monkeypatch.setattr(art, "ASCII_ART_PATH", missing_path)

    content = art.load_ascii_art()

    assert content == ""
