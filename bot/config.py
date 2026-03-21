"""Configuration module for the LMS Bot."""

import os
from pathlib import Path


class BotSettings:
    """Bot configuration loaded from environment variables."""

    def __init__(self) -> None:
        """Load settings from environment or .env file."""
        env_file = Path(__file__).parent.parent / ".env.bot.secret"
        if env_file.exists():
            self._load_env_file(env_file)

        # Telegram
        self.bot_token = os.environ.get("BOT_TOKEN", "")

        # LMS API
        self.lms_api_base_url = os.environ.get("LMS_API_BASE_URL", "")
        self.lms_api_key = os.environ.get("LMS_API_KEY", "")

        # LLM API
        self.llm_api_model = os.environ.get("LLM_API_MODEL", "coder-model")
        self.llm_api_key = os.environ.get("LLM_API_KEY", "")
        self.llm_api_base_url = os.environ.get("LLM_API_BASE_URL", "")

    def _load_env_file(self, path: Path) -> None:
        """Load environment variables from a .env file."""
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def load_settings() -> BotSettings:
    """Load and return bot settings."""
    return BotSettings()
