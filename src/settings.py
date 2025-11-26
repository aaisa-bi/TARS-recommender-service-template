from __future__ import annotations

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "local"
    api_key_hash: SecretStr | None = (
        "c9bc5884fe86a6255d97633cb65e61d4a73f7eca69206fdfdc692d5bc6c6ec67"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
