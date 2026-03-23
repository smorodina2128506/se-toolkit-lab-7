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

    def get_items(self) -> list | None:
        """Fetch items (labs and tasks) from the LMS API.

        Returns:
            List containing items data, or None if request failed.

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

    def get_pass_rates(self, lab: str) -> list | None:
        """Fetch pass rates for a specific lab.

        Args:
            lab: Lab identifier (e.g., "lab-04").

        Returns:
            List containing pass rates data, or None if request failed.

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

    def get_scores(self, lab: str) -> list | None:
        """Fetch score distribution for a specific lab.

        Args:
            lab: Lab identifier (e.g., "lab-04").

        Returns:
            List containing scores data, or None if request failed.

        Raises:
            httpx.RequestError: If the request fails.
        """
        if not self.base_url:
            msg = "LMS_API_BASE_URL not configured"
            raise httpx.RequestError(msg)

        url = f"{self.base_url.rstrip('/')}/analytics/scores"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._headers, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()

    def get_learners(self) -> list | None:
        """Fetch enrolled learners from the LMS API.

        Returns:
            List containing learners data, or None if request failed.

        Raises:
            httpx.RequestError: If the request fails.
        """
        if not self.base_url:
            msg = "LMS_API_BASE_URL not configured"
            raise httpx.RequestError(msg)

        url = f"{self.base_url.rstrip('/')}/learners/"
        with httpx.Client() as client:
            response = client.get(url, headers=self._headers, timeout=10.0)
            response.raise_for_status()
            return response.json()

    def get_timeline(self, lab: str) -> list | None:
        """Fetch timeline data for a specific lab.

        Args:
            lab: Lab identifier (e.g., "lab-04").

        Returns:
            List containing timeline data, or None if request failed.

        Raises:
            httpx.RequestError: If the request fails.
        """
        if not self.base_url:
            msg = "LMS_API_BASE_URL not configured"
            raise httpx.RequestError(msg)

        url = f"{self.base_url.rstrip('/')}/analytics/timeline"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._headers, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()

    def get_groups(self, lab: str) -> list | None:
        """Fetch group performance data for a specific lab.

        Args:
            lab: Lab identifier (e.g., "lab-04").

        Returns:
            List containing groups data, or None if request failed.

        Raises:
            httpx.RequestError: If the request fails.
        """
        if not self.base_url:
            msg = "LMS_API_BASE_URL not configured"
            raise httpx.RequestError(msg)

        url = f"{self.base_url.rstrip('/')}/analytics/groups"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._headers, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()

    def get_top_learners(self, lab: str, limit: int = 5) -> list | None:
        """Fetch top learners for a specific lab.

        Args:
            lab: Lab identifier (e.g., "lab-04").
            limit: Number of top learners to return.

        Returns:
            List containing top learners data, or None if request failed.

        Raises:
            httpx.RequestError: If the request fails.
        """
        if not self.base_url:
            msg = "LMS_API_BASE_URL not configured"
            raise httpx.RequestError(msg)

        url = f"{self.base_url.rstrip('/')}/analytics/top-learners"
        params = {"lab": lab, "limit": limit}
        with httpx.Client() as client:
            response = client.get(url, headers=self._headers, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()

    def get_completion_rate(self, lab: str) -> dict | None:
        """Fetch completion rate for a specific lab.

        Args:
            lab: Lab identifier (e.g., "lab-04").

        Returns:
            Dict containing completion rate data, or None if request failed.

        Raises:
            httpx.RequestError: If the request fails.
        """
        if not self.base_url:
            msg = "LMS_API_BASE_URL not configured"
            raise httpx.RequestError(msg)

        url = f"{self.base_url.rstrip('/')}/analytics/completion-rate"
        params = {"lab": lab}
        with httpx.Client() as client:
            response = client.get(url, headers=self._headers, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()

    def trigger_sync(self) -> dict | None:
        """Trigger ETL sync to refresh data.

        Returns:
            Dict containing sync status, or None if request failed.

        Raises:
            httpx.RequestError: If the request fails.
        """
        if not self.base_url:
            msg = "LMS_API_BASE_URL not configured"
            raise httpx.RequestError(msg)

        url = f"{self.base_url.rstrip('/')}/pipeline/sync"
        with httpx.Client() as client:
            response = client.post(url, headers=self._headers, json={}, timeout=30.0)
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
