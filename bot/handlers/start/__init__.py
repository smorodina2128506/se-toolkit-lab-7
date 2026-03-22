"""Handler for /start command."""


def handle_start() -> str:
    """Handle the /start command.

    Returns:
        Welcome message for the user.
    """
    return (
        "👋 Welcome to the LMS Bot!\n\n"
        "I can help you with:\n"
        "• View your lab scores\n"
        "• Check course information\n"
        "• Get help with commands\n\n"
        "Use /help to see all available commands."
    )
