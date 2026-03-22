"""Handler for /scores command."""

import httpx

from config import load_settings
from services.lms_client import LmsClient


def handle_scores(lab: str | None = None) -> str:
    """Handle the /scores command.

    Args:
        lab: Optional lab identifier to filter scores.

    Returns:
        Scores information for the user.
    """
    if not lab:
        return (
            "📊 Usage: /scores <lab-name>\n\n"
            "Example: /scores lab-04\n\n"
            "Use /labs to see available labs."
        )

    settings = load_settings()
    client = LmsClient(settings)

    try:
        pass_rates = client.get_pass_rates(lab)

        if not pass_rates:
            return f"📊 No scores available for {lab}."

        # Handle different response formats
        if isinstance(pass_rates, list):
            rates = pass_rates
        elif isinstance(pass_rates, dict):
            rates = pass_rates.get("results", pass_rates.get("data", [pass_rates]))
        else:
            return f"📊 No scores available for {lab}."

        if not rates:
            return f"📊 No scores available for {lab}."

        response = f"📊 Pass rates for {lab}:\n\n"
        for rate in rates:
            if isinstance(rate, dict):
                task_name = rate.get("task_name", rate.get("task", rate.get("name", "Unknown")))
                pass_rate = rate.get("pass_rate", rate.get("passRate", rate.get("rate", 0)))
                attempts = rate.get("attempts", rate.get("total_attempts", 0))

                # Format percentage
                if isinstance(pass_rate, float):
                    percentage = f"{pass_rate * 100:.1f}%"
                else:
                    percentage = f"{pass_rate}%"

                response += f"• {task_name}: {percentage} ({attempts} attempts)\n"

        return response

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"📊 Lab '{lab}' not found. Use /labs to see available labs."
        return f"❌ Failed to fetch scores: HTTP {e.response.status_code}. {e}"
    except httpx.RequestError as e:
        return f"❌ Failed to fetch scores: {e}. Check that the backend is running."
    except Exception as e:
        return f"❌ Failed to fetch scores: {e}"
