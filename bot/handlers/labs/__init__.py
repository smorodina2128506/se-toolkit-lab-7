"""Handler for /labs command."""

import httpx

from config import load_settings
from services.lms_client import LmsClient


def handle_labs() -> str:
    """Handle the /labs command.

    Returns:
        List of available labs.
    """
    settings = load_settings()
    client = LmsClient(settings)

    try:
        items = client.get_items()

        if not items:
            return "📚 No labs available at the moment."

        # Group items by lab
        labs = {}
        for item in items:
            lab_id = item.get("lab_id", item.get("id", "unknown"))
            lab_name = item.get("lab_name", item.get("name", "Unknown Lab"))
            if lab_id not in labs:
                labs[lab_id] = lab_name

        if not labs:
            return "📚 No labs available at the moment."

        response = "📚 Available labs:\n\n"
        for lab_id, lab_name in sorted(labs.items()):
            response += f"• {lab_id} — {lab_name}\n"

        return response

    except httpx.RequestError as e:
        return f"❌ Failed to fetch labs: {e}. Check that the backend is running."
    except Exception as e:
        return f"❌ Failed to fetch labs: {e}"
