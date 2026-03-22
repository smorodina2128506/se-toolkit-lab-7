"""Handler for /help command."""


def handle_help() -> str:
    """Handle the /help command.

    Returns:
        List of available commands and their descriptions.
    """
    return (
        "📚 Available Commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/health - Check bot and backend status\n"
        "/scores <lab> - View scores for a specific lab\n\n"
        "You can also ask questions in natural language:\n"
        "• What labs are available?\n"
        "• Show my progress\n"
        "• When is the next deadline?"
    )
