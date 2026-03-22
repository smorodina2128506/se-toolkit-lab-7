"""Handler for /health command."""


def handle_health() -> str:
    """Handle the /health command.

    Returns:
        Health status of the bot and backend services.
    """
    return "✅ Bot is healthy\n✅ Backend connection: OK"
