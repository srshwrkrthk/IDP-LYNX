from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    lynx_api_url: str = "http://127.0.0.1:8000"
    lynx_agent_token: str
    lynx_poll_interval: float = 1.0
    lynx_hid_window_seconds: float = 5.0

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = AgentSettings()