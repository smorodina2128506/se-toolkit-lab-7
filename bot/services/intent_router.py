"""Intent router for natural language queries."""

import re

from config import load_settings
from services.llm_service import LlmService


# Patterns for fallback handling
GREETING_PATTERNS = [
    r"^hi$", r"^hello$", r"^hey$", r"^good (morning|afternoon|evening)$",
    r"^greetings$", r"^howdy$",
]

HELP_PATTERNS = [
    r"^help$", r"^what can you do$", r"^commands$", r"^what are you capable",
]


def is_greeting(text: str) -> bool:
    """Check if text is a greeting."""
    text_lower = text.lower().strip()
    return any(re.match(pattern, text_lower) for pattern in GREETING_PATTERNS)


def is_help_request(text: str) -> bool:
    """Check if text is asking for help."""
    text_lower = text.lower().strip()
    return any(re.search(pattern, text_lower) for pattern in HELP_PATTERNS)


def is_gibberish(text: str) -> bool:
    """Check if text appears to be gibberish."""
    text = text.strip()
    
    # Too short
    if len(text) < 3:
        return True
    
    # No vowels
    if not any(c in text.lower() for c in "aeiou"):
        return True
    
    # All special characters
    if not any(c.isalnum() for c in text):
        return True
    
    # Repeated characters (like "asdfgh")
    if len(text) >= 4 and text.lower() in ["asdfgh", "asdf", "qwerty", "zzzz", "aaaa"]:
        return True
    
    return False


def get_capabilities_hint() -> str:
    """Return a hint about bot capabilities."""
    return (
        "I'm an LMS assistant bot. I can help you with:\n\n"
        "• Listing available labs\n"
        "• Showing scores and pass rates for specific labs\n"
        "• Finding top learners\n"
        "• Comparing group performance\n"
        "• Viewing submission timelines\n\n"
        "Try asking:\n"
        "• 'What labs are available?'\n"
        "• 'Show me scores for lab 4'\n"
        "• 'Which lab has the lowest pass rate?'\n"
        "• 'Who are the top 5 students in lab 4?'"
    )


def get_help_message() -> str:
    """Return help message with available commands."""
    return (
        "📚 Available Commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/health - Check backend status\n"
        "/labs - List all available labs\n"
        "/scores <lab> - View pass rates for a specific lab\n\n"
        "Or ask in natural language:\n"
        "• 'What labs are available?'\n"
        "• 'Show me scores for lab 4'\n"
        "• 'Which lab has the lowest pass rate?'\n"
        "• 'Who are the top 5 students?'"
    )


def route_natural_language(message: str) -> str:
    """Route a natural language message using LLM.

    Args:
        message: User's natural language query.

    Returns:
        Formatted response text.
    """
    # Handle special cases first
    if is_gibberish(message):
        return (
            "I didn't quite understand that. " + get_capabilities_hint()
        )

    if is_greeting(message):
        return (
            "Hello! 👋 I'm your LMS assistant. " + get_capabilities_hint()
        )

    if is_help_request(message):
        return get_help_message()

    # Use LLM for routing
    try:
        settings = load_settings()
        llm = LlmService(settings)
        return llm.route(message)
    except Exception as e:
        # Fallback if LLM fails
        return (
            f"I encountered an error processing your request: {e}\n\n"
            "You can try using commands directly:\n"
            "/labs - List available labs\n"
            "/scores <lab> - View scores for a lab\n"
            "/help - Show all commands"
        )
