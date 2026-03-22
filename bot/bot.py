#!/usr/bin/env python3
"""LMS Telegram Bot entry point.

Usage:
    python bot.py              # Run in Telegram mode (requires BOT_TOKEN)
    python bot.py --test       # Run in test mode (interactive CLI)
    python bot.py --test "/start"  # Run single command in test mode
"""

import argparse
import sys
from pathlib import Path

# Add bot directory to path for imports when running from bot/
bot_dir = Path(__file__).parent
sys.path.insert(0, str(bot_dir))

from config import load_settings
from handlers.health import handle_health
from handlers.help import handle_help
from handlers.labs import handle_labs
from handlers.scores import handle_scores
from handlers.start import handle_start


def parse_command(command: str) -> tuple[str, str | None]:
    """Parse a command string into command and argument.

    Args:
        command: The command string (e.g., "/scores lab-04").

    Returns:
        Tuple of (command_name, argument).
    """
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None
    return cmd, arg


def handle_command(command: str) -> str:
    """Route a command to the appropriate handler.

    Args:
        command: The command string to handle.

    Returns:
        Response text from the handler.
    """
    cmd, arg = parse_command(command)

    match cmd:
        case "/start" | "start":
            return handle_start()
        case "/help" | "help":
            return handle_help()
        case "/health" | "health":
            return handle_health()
        case "/labs" | "labs":
            return handle_labs()
        case "/scores" | "scores":
            return handle_scores(arg)
        case _:
            # Natural language query - route to LLM
            return f"I received your message: {command}\n\n(This will be processed by LLM in future iterations)"


def run_test_mode(command: str | None = None) -> int:
    """Run bot in test mode.

    Args:
        command: Optional command to execute. If None, runs interactive mode.

    Returns:
        Exit code (0 for success).
    """
    if command:
        # Single command mode
        response = handle_command(command)
        print(response)
        return 0

    # Interactive mode
    print("🤖 LMS Bot Test Mode")
    print("Type commands (e.g., /start, /help, /scores lab-04)")
    print("Type 'quit' or 'exit' to stop\n")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return 0

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            return 0

        if not user_input:
            continue

        response = handle_command(user_input)
        print(response)
        print()

    return 0


def run_telegram_mode() -> int:
    """Run bot in Telegram mode.

    Returns:
        Exit code (0 for success).
    """
    try:
        from aiogram import Bot, Dispatcher
    except ImportError:
        print("Error: aiogram not installed. Run: uv sync", file=sys.stderr)
        return 1

    settings = load_settings()

    if not settings.bot_token:
        print("Error: BOT_TOKEN not set in .env.bot.secret", file=sys.stderr)
        return 1

    # TODO: Implement Telegram bot
    print("Telegram mode not yet implemented.")
    print("Bot would connect with token:", settings.bot_token[:10] + "...")
    return 0


def main() -> int:
    """Main entry point.

    Returns:
        Exit code.
    """
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        nargs="?",
        const="",
        metavar="COMMAND",
        help="Run in test mode. Optionally provide a command to execute.",
    )

    args = parser.parse_args()

    if args.test is not None:
        # Test mode
        command = args.test if args.test else None
        return run_test_mode(command)
    else:
        # Telegram mode
        return run_telegram_mode()


if __name__ == "__main__":
    sys.exit(main())
