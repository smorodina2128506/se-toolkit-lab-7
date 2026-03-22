"""Handler for /scores command."""


def handle_scores(lab: str | None = None) -> str:
    """Handle the /scores command.

    Args:
        lab: Optional lab identifier to filter scores.

    Returns:
        Scores information for the user.
    """
    if lab:
        return f"📊 Scores for {lab}:\n\nNo scores available yet. Check back later!"
    return (
        "📊 Your Scores:\n\n"
        "No scores available yet. Complete some labs to see your progress here!"
    )
