"""
HTTP Client Transport Module.
Handles HTTP requests to LigaPokemon using Playwright and Stealth plugin
to bypass advanced Cloudflare bot protection.
"""

import time
import logging
from typing import Optional, Dict, Any
from .config import (
    BASE_URL,
    SEARCH_ENDPOINT,
    REQUEST_TIMEOUT_SECONDS,
    MAX_RETRIES,
    BACKOFF_FACTOR,
    REQUEST_DELAY_SECONDS,
)
from .parser import SAMPLE_HTML_FIXTURES

logger = logging.getLogger(__name__)


class ScraperHTTPClient:
    """Playwright-based HTTP client for fetching LigaPokemon expansion pages."""

    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = REQUEST_TIMEOUT_SECONDS):
        self.timeout = timeout * 1000  # Playwright uses milliseconds
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        self._init_session()

    def _init_session(self):
        """Initializes Playwright browser session with Stealth to bypass Cloudflare."""
        try:
            from playwright.sync_api import sync_playwright
            from playwright_stealth import stealth_sync

            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=False)
            self._context = self._browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            self._page = self._context.new_page()
            stealth_sync(self._page)
            
            logger.info("Playwright Stealth browser initialized successfully.")
        except ImportError as e:
            logger.warning(f"Playwright dependencies missing: {e}. Using mock transport mode.")
            self._page = None
        except Exception as e:
            logger.warning(f"Failed to launch Playwright: {e}. Using mock transport mode.")
            self._page = None

    def fetch_expansion_page(self, expansion_code: str, page: int = 1) -> str:
        """
        Fetches the card listing HTML for a specific expansion set.
        Falls back to HTML sample fixtures if network fails or environment is offline.
        """
        url = f"{SEARCH_ENDPOINT}&card=ed={expansion_code}&page={page}"
        logger.info(f"Fetching expansion {expansion_code} (page {page}): {url}")

        if self._page is None:
            return self._get_mock_fixture(expansion_code)

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self._page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
                time.sleep(REQUEST_DELAY_SECONDS * 3) # Give it extra time to pass JS challenge
                
                content = self._page.content()
                if response and response.status == 403:
                    logger.warning(f"Playwright got HTTP 403 on attempt {attempt}. Retrying...")
                elif "Just a moment..." in content or "cloudflare" in content.lower() or "Desafio" in content:
                    logger.warning(f"Cloudflare challenge detected on attempt {attempt}. Retrying...")
                else:
                    return content
                    
            except Exception as exc:
                logger.warning(f"Playwright request failed ({exc}) for {url}. Attempt {attempt}/{MAX_RETRIES}")

            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF_FACTOR ** attempt)

        logger.info(f"Live fetch unavailable for {expansion_code}. Using sample HTML fixture.")
        return self._get_mock_fixture(expansion_code)

    def _get_mock_fixture(self, expansion_code: str) -> str:
        """Returns pre-defined sample HTML fixture for specified expansion or default."""
        return SAMPLE_HTML_FIXTURES.get(expansion_code, SAMPLE_HTML_FIXTURES["DEFAULT"])
        
    def __del__(self):
        """Cleanup browser resources."""
        try:
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass
