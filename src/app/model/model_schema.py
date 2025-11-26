from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: str = Field(..., description="Unique event identifier")
    event_metadata: Dict[str, Any] = Field(default_factory=dict)
    user_metadata: Dict[str, Any] = Field(default_factory=dict)


class ActionResponse(BaseModel):
    action_channel: str
    action_metadata: Dict[str, Any]


class Recommender(ABC):
    @abstractmethod
    def recommend(self, event: Event) -> list[ActionResponse]:
        """
        Return recommended actions for the provided event.
        """
        raise NotImplementedError
