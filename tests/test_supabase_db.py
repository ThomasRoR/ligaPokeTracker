"""
Unit and Integration Tests for Supabase Database Client (`scraper/supabase_db.py`).
Verifies expansion creation, card catalog upsertion, time-series price snapshots,
latest prices view querying, and end-to-end mock flow execution (Requirement R2 & AC2).
"""

import os
import sys
import unittest

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scraper.supabase_db import SupabaseDB


class TestSupabaseDB(unittest.TestCase):
    """Test suite for SupabaseDB interface operating in offline/mock mode or live backend."""

    def setUp(self):
        self.db = SupabaseDB()  # Defaults to Mock Mode when env keys are unconfigured

    def test_get_or_create_expansion(self):
        """Test expansion creation and retrieval idempotency."""
        exp_id1 = self.db.get_or_create_expansion(
            name="XY - Roaring Skies", code="ROS", release_date="2015-05-06"
        )
        self.assertIsInstance(exp_id1, int)
        self.assertGreater(exp_id1, 0)

        # Retrieve existing expansion by code
        exp_id2 = self.db.get_or_create_expansion(
            name="XY - Roaring Skies Duplicate", code="ROS"
        )
        self.assertEqual(exp_id1, exp_id2, "Querying existing set code should return identical ID")

    def test_upsert_card(self):
        """Test card catalog insertion and upsert behavior."""
        exp_id = self.db.get_or_create_expansion(name="XY - Evolutions", code="EVO")
        card_id1 = self.db.upsert_card(
            expansion_id=exp_id,
            card_number="13/108",
            name="M Charizard EX",
            rarity="Ultra Rara",
            image_url="https://repositorio.ligapokemon.com.br/images/cartas/EVO/13.jpg",
        )
        self.assertIsInstance(card_id1, int)
        self.assertGreater(card_id1, 0)

        # Re-upserting same card should yield same card ID
        card_id2 = self.db.upsert_card(
            expansion_id=exp_id,
            card_number="13/108",
            name="M Charizard EX",
            rarity="Ultra Rara",
        )
        self.assertEqual(card_id1, card_id2)

    def test_insert_and_retrieve_price_history(self):
        """Test single and batch price snapshot insertions and price history queries."""
        exp_id = self.db.get_or_create_expansion(name="XY - Primal Clash", code="PRC")
        card_id = self.db.upsert_card(
            expansion_id=exp_id,
            card_number="55/160",
            name="Primal Kyogre EX",
        )

        # Insert single snapshot
        snap1 = self.db.insert_price_snapshot(
            card_id=card_id, price_min=115.00, price_avg=140.00, currency="BRL"
        )
        self.assertIsNotNone(snap1)
        self.assertEqual(float(snap1["price_min"]), 115.00)

        # Batch insert snapshots
        batch = [
            {"card_id": card_id, "price_min": 110.00, "price_avg": 135.00, "currency": "BRL"},
            {"card_id": card_id, "price_min": 105.00, "price_avg": 130.00, "currency": "BRL"},
        ]
        inserted = self.db.insert_batch_price_snapshots(batch)
        self.assertEqual(len(inserted), 2)

        # Query history
        history = self.db.get_card_price_history(card_id=card_id, limit=10)
        self.assertGreaterEqual(len(history), 3)

    def test_get_latest_prices_view(self):
        """Test latest card prices aggregation view query."""
        exp_id = self.db.get_or_create_expansion(name="XY - Ancient Origins", code="AOR")
        card_id = self.db.upsert_card(
            expansion_id=exp_id, card_number="98/98", name="M Rayquaza EX"
        )
        self.db.insert_price_snapshot(card_id=card_id, price_min=220.00, price_avg=260.00)

        latest = self.db.get_latest_prices(expansion_code="AOR")
        self.assertGreaterEqual(len(latest), 1)
        self.assertEqual(latest[0]["card_name"], "M Rayquaza EX")
        self.assertEqual(float(latest[0]["price_min"]), 220.00)

    def test_connectivity_and_mock_flow(self):
        """Test mandatory R2 & AC2 end-to-end verification method."""
        result = self.db.test_connectivity_and_mock_flow()
        self.assertTrue(result, "test_connectivity_and_mock_flow must return True")


if __name__ == "__main__":
    unittest.main()
