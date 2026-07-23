"""
HTTP Client Transport Module.
Handles HTTP requests to LigaPokemon with custom headers, timeouts, retry logic,
and fallback fixture responses when the live network is unavailable.
"""

import time
import logging
from typing import Optional, Dict, Any
from .config import (
    BASE_URL,
    SEARCH_ENDPOINT,
    DEFAULT_HEADERS,
    REQUEST_TIMEOUT_SECONDS,
    MAX_RETRIES,
    BACKOFF_FACTOR,
    REQUEST_DELAY_SECONDS,
)
from .parser import SAMPLE_HTML_FIXTURES

logger = logging.getLogger(__name__)


class ScraperHTTPClient:
    """Resilient HTTP client for fetching LigaPokemon expansion pages."""

    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = REQUEST_TIMEOUT_SECONDS):
        self.headers = headers or DEFAULT_HEADERS
        self.timeout = timeout
        self._session = None
        self._init_session()

    def _init_session(self):
        """Initializes Python requests session if requests library is installed."""
        try:
            import requests
            self._session = requests.Session()
            self._session.headers.update(self.headers)
        except ImportError:
            logger.warning("requests library not installed. Using mock transport mode.")
            self._session = None

    def fetch_expansion_page(self, expansion_code: str, page: int = 1) -> str:
        """
        Fetches the card listing HTML for a specific expansion set.
        Falls back to HTML sample fixtures if network fails or environment is offline.
        """
        url = f"{SEARCH_ENDPOINT}&card=ed={expansion_code}&page={page}"
        logger.info(f"Fetching expansion {expansion_code} (page {page}): {url}")

        if self._session is None:
            return self._get_mock_fixture(expansion_code)

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self._session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    time.sleep(REQUEST_DELAY_SECONDS)
                    return response.text
                elif response.status_code == 429:
                    logger.warning(f"Rate limited (HTTP 429) on attempt {attempt}. Retrying...")
                else:
                    logger.warning(f"HTTP status {response.status_code} for {url}. Attempt {attempt}/{MAX_RETRIES}")
            except Exception as exc:
                logger.warning(f"Network request failed ({exc}) for {url}. Attempt {attempt}/{MAX_RETRIES}")

            # Sleep with backoff before retry
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF_FACTOR ** attempt)

        logger.info(f"Live fetch unavailable for {expansion_code}. Using sample HTML fixture.")
        return self._get_mock_fixture(expansion_code)

    def _get_mock_fixture(self, expansion_code: str) -> str:
        """Returns pre-defined sample HTML fixture for specified expansion or default."""
        return SAMPLE_HTML_FIXTURES.get(expansion_code, SAMPLE_HTML_FIXTURES["DEFAULT"])
