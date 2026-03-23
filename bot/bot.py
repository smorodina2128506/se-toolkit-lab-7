#!/usr/bin/env python3
"""LMS Telegram Bot entry point.

Usage:
    python bot.py              # Run in Telegram mode (requires BOT_TOKEN)
    python bot.py --test       # Run in test mode (interactive CLI)
    python bot.py --test "/start"  # Run single command in test mode
    python bot.py --test "what labs are available"  # Natural language query
"""

import argparse
import sys
from pathlib import Path

# Add bot directory to path for imports when running from bot/
bot_dir = Path(__file__).parent
sys.path.insert(0, str(bot_dir))

from config import load_settings
from handlers.start import handle_start
from handlers.help import handle_help
from handlers.health import handle_health
from handlers.labs import handle_labs
from handlers.scores import handle_scores
from services.intent_router import route_natural_language


# Inline keyboard buttons for common actions
KEYBOARD_BUTTONS = [
    [{"text": "📚 Available Labs", "callback_data": "labs"}, {"text": "📊 My Scores", "callback_data": "scores"}],
    [{"text": "❤️ Health Check", "callback_data": "health"}, {"text": "❓ Help", "callback_data": "help"}],
    [{"text": "🏆 Top Students", "callback_data": "top_learners_lab-04"}],
    [{"text": "📈 Lab Timeline", "callback_data": "timeline_lab-04"}],
]


def get_keyboard_markup() -> list:
    """Get inline keyboard markup."""
    return KEYBOARD_BUTTONS


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


def is_natural_language(text: str) -> bool:
    """Check if text is natural language (not a slash command)."""
    text = text.strip()
    return not text.startswith("/")


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
            # Unknown command - suggest /help
            return f"❓ Unknown command: {command}\n\nUse /help to see available commands."


def handle_message(message: str) -> str:
    """Handle a message (command or natural language).

    Args:
        message: The message to handle.

    Returns:
        Response text.
    """
    if is_natural_language(message):
        return route_natural_language(message)
    else:
        return handle_command(message)


def run_test_mode(command: str | None = None) -> int:
    """Run bot in test mode.

    Args:
        command: Optional command to execute. If None, runs interactive mode.

    Returns:
        Exit code (0 for success).
    """
    if command:
        # Single command mode
        response = handle_message(command)
        print(response)
        return 0

    # Interactive mode
    print("🤖 LMS Bot Test Mode")
    print("Type commands (e.g., /start, /help, /scores lab-04)")
    print("Or natural language (e.g., 'what labs are available')")
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

        response = handle_message(user_input)
        print(response)
        print()

    return 0


def run_telegram_mode() -> int:
    """Run bot in Telegram mode.

    Returns:
        Exit code (0 for success).
    """
    try:
        from aiogram import Bot, Dispatcher, types
        from aiogram.filters import Command
    except ImportError:
        print("Error: aiogram not installed. Run: uv sync", file=sys.stderr)
        return 1

    import asyncio

    settings = load_settings()

    if not settings.bot_token:
        print("Error: BOT_TOKEN not set in .env.bot.secret", file=sys.stderr)
        return 1

    async def cmd_start(message: types.Message) -> None:
        """Handle /start command."""
        response = handle_start()
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text=btn["text"], callback_data=btn["callback_data"]) for btn in row]
                for row in KEYBOARD_BUTTONS
            ]
        )
        await message.answer(response, reply_markup=keyboard)

    async def cmd_help(message: types.Message) -> None:
        """Handle /help command."""
        response = handle_help()
        await message.answer(response)

    async def cmd_health(message: types.Message) -> None:
        """Handle /health command."""
        response = handle_health()
        await message.answer(response)

    async def cmd_labs(message: types.Message) -> None:
        """Handle /labs command."""
        response = handle_labs()
        await message.answer(response)

    async def cmd_scores(message: types.Message) -> None:
        """Handle /scores command."""
        args = message.text.split(maxsplit=1)
        lab = args[1] if len(args) > 1 else None
        response = handle_scores(lab)
        await message.answer(response)

    async def handle_text(message: types.Message) -> None:
        """Handle natural language messages."""
        text = message.text or ""
        response = handle_message(text)
        await message.answer(response)

    async def handle_callback(message: types.CallbackQuery) -> None:
        """Handle inline keyboard button clicks."""
        callback_data = message.data or ""
        
        # Map callback data to commands
        callback_map = {
            "labs": "/labs",
            "scores": "/scores lab-04",
            "health": "/health",
            "help": "/help",
        }
        
        # Handle lab-specific callbacks
        if callback_data.startswith("top_learners_"):
            lab = callback_data.replace("top_learners_", "")
            command = f"Show top 5 students in {lab}"
        elif callback_data.startswith("timeline_"):
            lab = callback_data.replace("timeline_", "")
            command = f"Show timeline for {lab}"
        else:
            command = callback_map.get(callback_data, "")
        
        if command:
            response = handle_message(command)
            await message.message.answer(response)
            await message.answer()

    async def main() -> None:
        """Main bot function."""
        bot = Bot(token=settings.bot_token)
        dp = Dispatcher()

        # Register handlers
        dp.message.register(cmd_start, Command("start"))
        dp.message.register(cmd_help, Command("help"))
        dp.message.register(cmd_health, Command("health"))
        dp.message.register(cmd_labs, Command("labs"))
        dp.message.register(cmd_scores, Command("scores"))
        dp.message.register(handle_text)
        dp.callback_query.register(handle_callback)

        print("Bot is running...")
        await dp.start_polling(bot)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")

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
