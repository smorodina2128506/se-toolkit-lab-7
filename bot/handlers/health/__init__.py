"""Handler for /health command."""

import httpx

from config import load_settings
from services.lms_client import LmsClient


def handle_health() -> str:
    """Handle the /health command.

    Returns:
        Health status of the bot and backend services.
    """
    settings = load_settings()
    client = LmsClient(settings)

    result = client.get_health()

    if result.get("healthy"):
        count = result.get("item_count", 0)
        return f"✅ Backend is healthy. {count} items available."

    error = result.get("error", "Unknown error")
    # Format error message in a user-friendly way
    if "connection refused" in error.lower() or "connect" in error.lower():
        return f"❌ Backend error: connection refused. Check that the services are running."
    if "502" in error or "bad gateway" in error.lower():
        return f"❌ Backend error: HTTP 502 Bad Gateway. The backend service may be down."
    if "401" in error or "unauthorized" in error.lower():
        return f"❌ Backend error: HTTP 401 Unauthorized. Check LMS_API_KEY configuration."
    if "404" in error or "not found" in error.lower():
        return f"❌ Backend error: HTTP 404 Not Found. Check LMS_API_BASE_URL configuration."

    return f"❌ Backend error: {error}. Check that the services are running."
