"""
Scraper Pipeline Orchestration Module.
Coordinates fetching, parsing, and database persistence for Pokémon Price Tracker.
Targeting 8 Mega Evolution block expansions (`PRC`, `ROS`, `AOR`, `BKT`, `BKP`, `FCO`, `STS`, `EVO`).
"""

import sys
import logging
from typing import List, Dict, Any, Optional

from .config import MEGA_EVOLUTION_EXPANSIONS
from .http_client import ScraperHTTPClient
from .parser import parse_cards_from_html
from .supabase_db import SupabaseDB

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ScraperPipeline")


def run_pipeline(
    expansion_codes: Optional[List[str]] = None,
    db_url: Optional[str] = None,
    db_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes the end-to-end scraping and persistence pipeline.
    
    Args:
        expansion_codes: List of expansion set codes to scrape (defaults to all 8 Mega Evolution sets).
        db_url: Optional Supabase URL override.
        db_key: Optional Supabase API key override.

    Returns:
        Summary dict containing counts of processed expansions, cards, and snapshots.
    """
    logger.info("Starting Pokémon Price Tracker Scraper Pipeline...")

    # Instantiate HTTP Transport Client & Database Client
    http_client = ScraperHTTPClient()
    db = SupabaseDB(url=db_url, key=db_key)

    # Filter target expansions
    if expansion_codes:
        targets = [
            e for e in MEGA_EVOLUTION_EXPANSIONS if e["code"].upper() in [c.upper() for c in expansion_codes]
        ]
    else:
        targets = MEGA_EVOLUTION_EXPANSIONS

    summary = {
        "expansions_processed": 0,
        "cards_upserted": 0,
        "price_snapshots_inserted": 0,
        "details": [],
    }

    for exp_meta in targets:
        code = exp_meta["code"]
        name = exp_meta["name"]
        release_date = exp_meta.get("release_date")

        logger.info(f"--- Processing Expansion: {name} ({code}) ---")

        # 1. Get or Create Expansion in Database
        exp_id = db.get_or_create_expansion(name=name, code=code, release_date=release_date)

        # 2. Fetch Expansion Card Listing HTML Page
        html_content = http_client.fetch_expansion_page(expansion_code=code, page=1)

        # 3. Parse Cards from HTML
        extracted_cards = parse_cards_from_html(html_content=html_content, expansion_code=code)
        logger.info(f"Extracted {len(extracted_cards)} cards for set {code}.")

        exp_card_count = 0
        exp_snap_count = 0

        # 4. Persist Cards & Price History Snapshots
        snapshots_to_batch = []
        for card_data in extracted_cards:
            card_id = db.upsert_card(
                expansion_id=exp_id,
                card_number=card_data["card_number"],
                name=card_data["name"],
                rarity=card_data.get("rarity"),
                image_url=card_data.get("image_url"),
            )
            exp_card_count += 1

            if card_data.get("price_min") is not None:
                snapshots_to_batch.append({
                    "card_id": card_id,
                    "price_min": card_data["price_min"],
                    "price_avg": card_data.get("price_avg"),
                    "currency": card_data.get("currency", "BRL"),
                })

        if snapshots_to_batch:
            inserted_snaps = db.insert_batch_price_snapshots(snapshots_to_batch)
            exp_snap_count += len(inserted_snaps)

        summary["expansions_processed"] += 1
        summary["cards_upserted"] += exp_card_count
        summary["price_snapshots_inserted"] += exp_snap_count
        summary["details"].append({
            "code": code,
            "name": name,
            "cards": exp_card_count,
            "snapshots": exp_snap_count,
        })

    logger.info("Pipeline execution finished successfully.")
    logger.info(
        f"Summary: Expansions={summary['expansions_processed']}, "
        f"Cards={summary['cards_upserted']}, "
        f"Snapshots={summary['price_snapshots_inserted']}"
    )

    return summary


if __name__ == "__main__":
    codes = sys.argv[1:] if len(sys.argv) > 1 else None
    run_pipeline(expansion_codes=codes)
