from pathlib import Path

import pytest

from app.model.model_schema import ActionResponse, Event, Recommender
from app.model.recommender import DefaultRecommender


def test_default_recommender_missing_config(tmp_path: Path) -> None:
    missing_config = tmp_path / "missing.yaml"
    rec = DefaultRecommender(missing_config)
    event = Event(id="evt", event_metadata={}, user_metadata={})

    result = rec.recommend(event)

    assert result == ActionResponse(
        action_channel="web",
        action_metadata={"message": "hello client"},
    )


def test_recommender_base_not_implemented() -> None:
    class BadRecommender(Recommender):
        def recommend(self, event: Event) -> ActionResponse:  # type: ignore[override]
            return super().recommend(event)

    rec = BadRecommender()
    with pytest.raises(NotImplementedError):
        rec.recommend(Event(id="evt", event_metadata={}, user_metadata={}))
