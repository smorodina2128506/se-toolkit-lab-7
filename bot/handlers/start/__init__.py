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
        "• Check available labs\n"
        "• Get backend status\n"
        "• Get help with commands\n\n"
        "You can use commands like /help, /labs, /scores\n"
        "Or just ask me questions in natural language!\n\n"
        "Try: 'What labs are available?' or 'Show me scores for lab 4'"
    )
