"""
Standalone test script located at `scraper/test_scraper.py` for direct execution.
Executes test suite for Scraper Engine and Supabase DB Client.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.test_scraper import TestScraperEngine
from tests.test_supabase_db import TestSupabaseDB


def main():
    """Runs scraper engine and database unit tests."""
    print("=" * 70)
    print("Running Pokémon Price Tracker Test Suite (`scraper/test_scraper.py`)")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestScraperEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestSupabaseDB))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n[SUCCESS] All tests passed cleanly.")
        sys.exit(0)
    else:
        print("\n[FAILURE] Some tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
