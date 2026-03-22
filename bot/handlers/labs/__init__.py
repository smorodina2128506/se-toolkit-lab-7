"""Handler for /labs command."""


def handle_labs() -> str:
    """Handle the /labs command.

    Returns:
        List of available labs.
    """
    return (
        "📚 Available Labs:\n\n"
        "• lab-01: Introduction\n"
        "• lab-02: Setup and Configuration\n"
        "• lab-03: Basic Commands\n"
        "• lab-04: Advanced Features\n\n"
        "Use /scores <lab-name> to view your score for a specific lab."
    )
