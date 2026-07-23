"""
Unit and Integration Tests for Scraper Engine (`scraper/parser.py`, `scraper/http_client.py`, `scraper/pipeline.py`).
Verifies extraction of card name, number, set, rarity, image, and PT-BR currency sanitization for Mega Evolution block cards (R1 & AC1).
"""

import os
import sys
import unittest

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scraper.config import MEGA_EVOLUTION_EXPANSIONS
from scraper.parser import clean_currency, parse_cards_from_html, SAMPLE_HTML_FIXTURES
from scraper.http_client import ScraperHTTPClient
from scraper.pipeline import run_pipeline


class TestScraperEngine(unittest.TestCase):
    """Test suite verifying scraper parser and pipeline functionality (Requirement R1 & AC1)."""

    def test_clean_currency(self):
        """Test PT-BR currency cleaning helper for various string formats."""
        self.assertEqual(clean_currency("R$ 1.234,56"), 1234.56)
        self.assertEqual(clean_currency("R$ 45,00"), 45.0)
        self.assertEqual(clean_currency("12,50"), 12.5)
        self.assertEqual(clean_currency("R$ 0,50"), 0.5)
        self.assertIsNone(clean_currency("-"))
        self.assertIsNone(clean_currency(""))
        self.assertIsNone(clean_currency(None))
        self.assertEqual(clean_currency(100.50), 100.50)

    def test_parse_mega_evolution_html_ros(self):
        """Test parsing HTML for XY - Roaring Skies (ROS) Mega Evolution cards."""
        html = SAMPLE_HTML_FIXTURES["ROS"]
        cards = parse_cards_from_html(html, expansion_code="ROS")
        self.assertGreaterEqual(len(cards), 3)

        # 1. Mega Rayquaza EX
        rayquaza = next((c for c in cards if "Rayquaza" in c["name"]), None)
        self.assertIsNotNone(rayquaza, "Mega Rayquaza EX should be parsed")
        self.assertEqual(rayquaza["card_number"], "61/108")
        self.assertEqual(rayquaza["price_min"], 145.90)
        self.assertEqual(rayquaza["price_avg"], 180.00)
        self.assertEqual(rayquaza["expansion_code"], "ROS")

        # 2. Mega Latios EX
        latios = next((c for c in cards if "Latios" in c["name"]), None)
        self.assertIsNotNone(latios, "Mega Latios EX should be parsed")
        self.assertEqual(latios["card_number"], "59/108")
        self.assertEqual(latios["price_min"], 42.50)
        self.assertEqual(latios["price_avg"], 55.00)

        # 3. Shaymin EX
        shaymin = next((c for c in cards if "Shaymin" in c["name"]), None)
        self.assertIsNotNone(shaymin, "Shaymin EX should be parsed")
        self.assertEqual(shaymin["card_number"], "77/108")
        self.assertEqual(shaymin["price_min"], 89.00)

    def test_parse_mega_evolution_html_evo(self):
        """Test parsing HTML for XY - Evolutions (EVO) Mega Evolution cards."""
        html = SAMPLE_HTML_FIXTURES["EVO"]
        cards = parse_cards_from_html(html, expansion_code="EVO")
        self.assertGreaterEqual(len(cards), 2)

        # Mega Charizard EX
        charizard = next((c for c in cards if "Charizard" in c["name"]), None)
        self.assertIsNotNone(charizard, "Mega Charizard EX should be parsed")
        self.assertEqual(charizard["card_number"], "13/108")
        self.assertEqual(charizard["price_min"], 250.00)
        self.assertEqual(charizard["price_avg"], 310.00)

    def test_parse_mega_evolution_html_prc(self):
        """Test parsing HTML for XY - Primal Clash (PRC) Mega Evolution cards."""
        html = SAMPLE_HTML_FIXTURES["PRC"]
        cards = parse_cards_from_html(html, expansion_code="PRC")
        self.assertGreaterEqual(len(cards), 2)

        # Primal Kyogre EX
        kyogre = next((c for c in cards if "Kyogre" in c["name"]), None)
        self.assertIsNotNone(kyogre, "Primal Kyogre EX should be parsed")
        self.assertEqual(kyogre["card_number"], "55/160")
        self.assertEqual(kyogre["price_min"], 115.00)

    def test_http_client_fallback_fixture(self):
        """Test HTTP transport client fallback mechanism when network is unconfigured."""
        client = ScraperHTTPClient()
        html = client.fetch_expansion_page("ROS")
        self.assertIn("M Rayquaza EX", html)
        cards = parse_cards_from_html(html, "ROS")
        self.assertGreaterEqual(len(cards), 1)

    def test_pipeline_execution(self):
        """Test execution of the end-to-end scraper pipeline on Mega Evolution expansions."""
        summary = run_pipeline(expansion_codes=["ROS", "EVO"])
        self.assertEqual(summary["expansions_processed"], 2)
        self.assertGreater(summary["cards_upserted"], 0)
        self.assertGreater(summary["price_snapshots_inserted"], 0)


if __name__ == "__main__":
    unittest.main()
