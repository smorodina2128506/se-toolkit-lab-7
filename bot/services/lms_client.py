"""LMS API Client Service."""

import httpx

from config import BotSettings


class LmsClient:
    """Client for interacting with the LMS API."""

    def __init__(self, settings: BotSettings) -> None:
        """Initialize LMS client.

        Args:
            settings: Bot configuration settings.
        """
        self.settings = settings
        self.base_url = settings.lms_api_base_url
        self.api_key = settings.lms_api_key
        self._headers = {"Authorization": f"Bearer {self.api_key}"}

    def get_items(self) -> dict | None:
        """Fetch items (labs and tasks) from the LMS API.

        Returns:
            Dictionary containing items data, or None if request failed.

        Raises:
            httpx.RequestError: If the request fails.
        """
        if not self.base_url:
            msg = "LMS_API_BASE_URL not configured"
            raise httpx.RequestError(msg)

        url = f"{self.base_url.rstrip('/')}/items/"
        with httpx.Client() as client:
            response = client.get(url, headers=self._headers, timeout=10.0)
            response.raise_for_status()
            return response.json()

    def get_pass_rates(self, lab: str) -> dict | None:
        """Fetch pass rates for a specific lab.

        Args:
            lab: Lab identifier (e.g., "lab-04").

        Returns:
            Dictionary containing pass rates data, or None if request failed.

        Raises:
            httpx.RequestError: If the request fails.
        """
        if not self.base_url:
            msg = "LMS_API_BASE_URL not configured"
            raise httpx.RequestError(msg)

        url = f"{self.base_url.rstrip('/')}/analytics/pass-rates"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._headers, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()

    def get_health(self) -> dict:
        """Check if the LMS API is healthy by fetching items.

        Returns:
            Dictionary with health status.
        """
        try:
            items = self.get_items()
            count = len(items) if items else 0
            return {"healthy": True, "item_count": count}
        except httpx.RequestError as e:
            return {"healthy": False, "error": str(e)}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
