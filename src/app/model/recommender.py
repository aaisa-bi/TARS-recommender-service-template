from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple

from loguru import logger
from omegaconf import DictConfig, OmegaConf

from app.model.model_schema import ActionResponse, Event, Recommender


class DefaultRecommender(Recommender):
    def __init__(self, config_path: Path) -> None:
        config = self._load_config(config_path)
        container = OmegaConf.to_container(config, resolve=True)
        self.config_data: Dict[str, Any] = container if isinstance(container, dict) else {}

    def _load_config(self, path: Path) -> DictConfig:
        if path.is_file():
            return OmegaConf.load(path)
        logger.warning("Config file {} not found. Using fallback configuration.", path)
        return OmegaConf.create({})

    def _get_action_defaults(self) -> Tuple[str, Dict[str, Any]]:
        action_config = (
            self.config_data.get("action") if isinstance(self.config_data, dict) else {}
        ) or {}
        channel = str(action_config.get("channel", "web"))
        message = str(action_config.get("message", "hello client"))
        return channel, {"message": message}

    def recommend(self, event: Event) -> ActionResponse:
        # Placeholder for future business logic using event details.
        default_action_channel, default_action_metadata = self._get_action_defaults()
        return ActionResponse(
            action_channel=default_action_channel,
            action_metadata=default_action_metadata,
        )
