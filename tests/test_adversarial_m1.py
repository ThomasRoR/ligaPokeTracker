"""
Adversarial Challenge Test Suite for Milestone 1.
Tests corner cases in currency parsing, edge cases in HTML parsing, and database layer boundary conditions.
"""

import os
import sys
import unittest

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scraper.parser import clean_currency, parse_cards_from_html
from scraper.supabase_db import SupabaseDB


class TestCurrencyParsingAdversarial(unittest.TestCase):
    """Adversarial challenge tests for clean_currency()."""

    def test_clean_currency_negative_values(self):
        """Corner Case: Negative currency values."""
        # String representations of negative currency values
        res1 = clean_currency("-10,00")
        res2 = clean_currency("R$ -10,00")
        res3 = clean_currency("-15.50")
        
        # Empirical test: check actual output
        # Record whether negative values preserve minus sign or strip it
        print(f"\n[EMPIRICAL] clean_currency('-10,00') -> {res1}")
        print(f"[EMPIRICAL] clean_currency('R$ -10,00') -> {res2}")
        print(f"[EMPIRICAL] clean_currency('-15.50') -> {res3}")
        
        # Negative numbers should be parsed as negative floats or return None if invalid,
        # but should NOT silently convert negative to positive!
        self.assertNotEqual(res1, 10.0, "clean_currency('-10,00') converted negative value to positive!")
        self.assertNotEqual(res2, 10.0, "clean_currency('R$ -10,00') converted negative value to positive!")

    def test_clean_currency_zero(self):
        """Corner Case: R$ 0,00 and numeric 0 / 0.0."""
        self.assertEqual(clean_currency("R$ 0,00"), 0.0)
        self.assertEqual(clean_currency("0,00"), 0.0)
        
        # Numeric 0 and 0.0
        res_int_zero = clean_currency(0)
        res_float_zero = clean_currency(0.0)
        print(f"[EMPIRICAL] clean_currency(0) -> {res_int_zero}")
        print(f"[EMPIRICAL] clean_currency(0.0) -> {res_float_zero}")
        
        self.assertEqual(res_int_zero, 0.0, "clean_currency(0) returned None due to truthy check failure!")
        self.assertEqual(res_float_zero, 0.0, "clean_currency(0.0) returned None due to truthy check failure!")

    def test_clean_currency_thousands_brl(self):
        """Corner Case: Thousands separators R$ 10.000,50."""
        self.assertEqual(clean_currency("R$ 10.000,50"), 10000.50)
        self.assertEqual(clean_currency("10.000,50"), 10000.50)
        self.assertEqual(clean_currency("R$ 1.234.567,89"), 1234567.89)

    def test_clean_currency_none_and_empty(self):
        """Corner Case: None and empty strings."""
        self.assertIsNone(clean_currency(None))
        self.assertIsNone(clean_currency(""))
        self.assertIsNone(clean_currency("   "))

    def test_clean_currency_malformed_strings(self):
        """Corner Case: Malformed string formats."""
        self.assertIsNone(clean_currency("R$ abc"))
        self.assertIsNone(clean_currency("abc"))
        self.assertIsNone(clean_currency("R$ --"))
        self.assertIsNone(clean_currency("N/A"))
        self.assertIsNone(clean_currency("null"))

    def test_clean_currency_multiple_separators(self):
        """Corner Case: Ambiguous or invalid multiple decimal/comma formats."""
        res1 = clean_currency("R$ 10,00,00")
        res2 = clean_currency("R$ 10.00.00")
        print(f"[EMPIRICAL] clean_currency('R$ 10,00,00') -> {res1}")
        print(f"[EMPIRICAL] clean_currency('R$ 10.00.00') -> {res2}")

    def test_clean_currency_boolean_and_containers(self):
        """Corner Case: Non-string data types (bool, list, dict)."""
        res_true = clean_currency(True)
        res_false = clean_currency(False)
        print(f"[EMPIRICAL] clean_currency(True) -> {res_true}")
        print(f"[EMPIRICAL] clean_currency(False) -> {res_false}")
        
        self.assertIsNone(res_true, "clean_currency(True) returned float 1.0 instead of None!")
        self.assertIsNone(res_false, "clean_currency(False) returned float/None improperly!")


class TestHTMLParsingAdversarial(unittest.TestCase):
    """Adversarial challenge tests for parse_cards_from_html()."""

    def test_parse_missing_price_elements(self):
        """Edge Case: Missing price elements in HTML DOM."""
        html = """
        <div class="card-listing-container">
            <div class="item-card" data-id="5001">
                <div class="card-name"><a href="/card1">Mega Rayquaza-EX</a></div>
                <div class="card-number">61/108</div>
                <div class="card-rarity">Ultra Rara</div>
                <div class="price-box">
                    <!-- Missing price spans -->
                </div>
            </div>
        </div>
        """
        cards = parse_cards_from_html(html, expansion_code="ROS")
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["name"], "Mega Rayquaza-EX")
        self.assertEqual(cards[0]["price_min"], 0.0)
        self.assertIsNone(cards[0]["price_avg"])

    def test_parse_broken_dom_structures(self):
        """Edge Case: Broken HTML DOM structures, unclosed tags, empty strings."""
        # Unclosed tags & broken markup
        broken_html = """
        <div class="item-card"><div class="card-name">Primal Kyogre-EX</div><div class="card-number">55/160</div>
        <span>Unclosed tag block without container
        """
        cards = parse_cards_from_html(broken_html, expansion_code="PRC")
        print(f"[EMPIRICAL] Broken DOM parsed {len(cards)} cards: {cards}")
        self.assertGreaterEqual(len(cards), 1)
        self.assertEqual(cards[0]["name"], "Primal Kyogre-EX")

        # Empty HTML / None
        self.assertEqual(parse_cards_from_html("", "ROS"), [])
        self.assertEqual(parse_cards_from_html("   ", "ROS"), [])
        self.assertEqual(parse_cards_from_html(None, "ROS"), [])

    def test_parse_special_characters_in_card_names(self):
        """Edge Case: Special characters in card names."""
        html = """
        <div class="card-listing-container">
            <div class="item-card">
                <div class="card-name"><a href="/c1">Mega Rayquaza-EX &amp; Primal Kyogre-EX</a></div>
                <div class="card-number">101/108</div>
                <div class="price-box"><span class="preco-menor">R$ 50,00</span></div>
            </div>
            <div class="item-card">
                <div class="card-name"><a href="/c2">Flabébé &lt;Special&gt; "Shiny" 'Art'</a></div>
                <div class="card-number">102/108</div>
                <div class="price-box"><span class="preco-menor">R$ 15,00</span></div>
            </div>
            <div class="item-card">
                <div class="card-name"><a href="/c3">Nidoran ♀ / Nidoran ♂</a></div>
                <div class="card-number">103/108</div>
                <div class="price-box"><span class="preco-menor">R$ 5,00</span></div>
            </div>
        </div>
        """
        cards = parse_cards_from_html(html, expansion_code="TEST")
        self.assertEqual(len(cards), 3)
        self.assertEqual(cards[0]["name"], "Mega Rayquaza-EX & Primal Kyogre-EX")
        self.assertEqual(cards[1]["name"], 'Flabébé <Special> "Shiny" \'Art\'')
        self.assertEqual(cards[2]["name"], "Nidoran ♀ / Nidoran ♂")

    def test_parse_card_without_number_and_without_price(self):
        """Edge Case: Card entry with name but missing BOTH number and price."""
        html = """
        <div class="card-listing-container">
            <div class="item-card">
                <div class="card-name"><a href="/c1">Ghost Card</a></div>
                <!-- Missing number and missing price -->
            </div>
        </div>
        """
        cards = parse_cards_from_html(html, expansion_code="TEST")
        print(f"[EMPIRICAL] Card without number and price parsed: {cards}")
        # Evaluate if card is dropped silently
        self.assertEqual(len(cards), 0, "Card without number or price was silently included or dropped unexpectedly.")


class TestSupabaseDBAdversarial(unittest.TestCase):
    """Adversarial challenge tests for SupabaseDB."""

    def setUp(self):
        self.db = SupabaseDB()

    def test_db_duplicate_card_upserts(self):
        """Edge Case: Duplicate card upserts and case/whitespace variations."""
        exp_id = self.db.get_or_create_expansion(name="XY - Roaring Skies", code="ROS")

        # 1. Standard upsert
        cid1 = self.db.upsert_card(exp_id, "61/108", "M Rayquaza EX")
        # 2. Re-upsert identical
        cid2 = self.db.upsert_card(exp_id, "61/108", "M Rayquaza EX")
        self.assertEqual(cid1, cid2)

        # 3. Re-upsert with trailing whitespace (should match due to strip())
        cid3 = self.db.upsert_card(exp_id, "61/108 ", " M Rayquaza EX ")
        self.assertEqual(cid1, cid3)

        # 4. Re-upsert with different casing
        cid4 = self.db.upsert_card(exp_id, "61/108", "m rayquaza ex")
        self.assertEqual(cid1, cid4, "Card upsert with different casing should return identical card ID")

    def test_db_null_and_invalid_prices(self):
        """Edge Case: Null prices, negative prices, type errors in insert_price_snapshot."""
        exp_id = self.db.get_or_create_expansion(name="XY - Evolutions", code="EVO")
        card_id = self.db.upsert_card(exp_id, "13/108", "M Charizard EX")

        # 1. price_min is None
        res_null = self.db.insert_price_snapshot(card_id, price_min=None)
        self.assertIsNone(res_null["price_min"])

        # 2. price_min is string "250.00"
        res_str = self.db.insert_price_snapshot(card_id, price_min="250.00", price_avg="310.00")
        self.assertEqual(res_str["price_min"], 250.00)

        # 3. price_min is negative -10.00
        res_neg = self.db.insert_price_snapshot(card_id, price_min=-10.00)
        self.assertEqual(res_neg["price_min"], -10.00)

    def test_db_empty_and_invalid_batch(self):
        """Edge Case: Empty batch array and missing keys in batch item."""
        # 1. Empty batch array
        res_empty = self.db.insert_batch_price_snapshots([])
        self.assertEqual(res_empty, [])

        # 2. Batch item missing mandatory key 'price_min'
        res_batch_missing = self.db.insert_batch_price_snapshots([{"card_id": 99}])
        self.assertEqual(len(res_batch_missing), 1)
        self.assertIsNone(res_batch_missing[0]["price_min"])

    def test_db_missing_mandatory_fields(self):
        """Edge Case: Mandatory fields passed as None or empty strings."""
        # 1. code=None in get_or_create_expansion
        exp_id_none_code = self.db.get_or_create_expansion(name="Set Without Code", code=None)
        self.assertGreater(exp_id_none_code, 0)

        # 2. card_number=None or name=None in upsert_card
        exp_id = self.db.get_or_create_expansion(name="XY - Set", code="XY1")
        cid_none_num = self.db.upsert_card(exp_id, card_number=None, name="Card Name")
        self.assertGreater(cid_none_num, 0)

        cid_none_name = self.db.upsert_card(exp_id, card_number="001", name=None)
        self.assertGreater(cid_none_name, 0)


if __name__ == "__main__":
    unittest.main()
