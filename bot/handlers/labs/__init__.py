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

        # Group items by lab - try multiple field names
        labs = {}
        for item in items:
            # Try different field names for lab id
            lab_id = (
                item.get("lab_id")
                or item.get("lab")
                or item.get("id")
                or "unknown"
            )
            
            # Try different field names for lab name
            lab_name = (
                item.get("lab_name")
                or item.get("name")
                or item.get("title")
                or item.get("description")
                or f"Lab {lab_id}"
            )
            
            # Convert lab_id to standard format if needed
            if isinstance(lab_id, int):
                lab_id = f"lab-{lab_id:02d}"
            
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
