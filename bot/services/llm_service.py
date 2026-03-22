"""LLM Service for natural language processing."""

from config import BotSettings


class LlmService:
    """Service for interacting with LLM API."""

    def __init__(self, settings: BotSettings) -> None:
        """Initialize LLM service.

        Args:
            settings: Bot configuration settings.
        """
        self.settings = settings

    def query(self, prompt: str) -> str:
        """Send a query to the LLM API.

        Args:
            prompt: The user's query or message.

        Returns:
            LLM response text.
        """
        # TODO: Implement actual LLM API call
        return f"LLM response to: {prompt}"
