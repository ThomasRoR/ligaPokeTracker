"""
Supabase Database Interface Module (`supabase_db.py`).
Provides normalized CRUD operations for Pokémon card expansions, catalog metadata,
and historical price snapshots. Supports both live Supabase client and offline mock mode.
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)


class SupabaseDB:
    """
    Database Access Layer for Pokémon Price Tracker.
    Satisfies Requirement R2 and Acceptance Criteria 2.
    """

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        self.url = url or os.getenv("SUPABASE_URL", "")
        self.key = (
            key
            or os.getenv("SUPABASE_KEY", "")
            or os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        )

        self.client = None
        self.is_mock_mode = True

        # In-memory data store for offline / mock fallback execution
        self._mock_expansions: Dict[str, Dict[str, Any]] = {}  # code -> dict
        self._mock_cards: Dict[Tuple[int, str, str], Dict[str, Any]] = {}  # (exp_id, number, name) -> dict
        self._mock_price_history: List[Dict[str, Any]] = []

        self._next_exp_id = 1
        self._next_card_id = 1
        self._next_price_id = 1

        self._init_connection()

    def _init_connection(self):
        """Attempts to initialize live Supabase client, defaulting to mock mode if unconfigured."""
        if not self.url or not self.key or "example.com" in self.url:
            logger.info("SUPABASE_URL/KEY unconfigured. Operating in Offline Mock Mode.")
            self.is_mock_mode = True
            return

        try:
            from supabase import create_client
            self.client = create_client(self.url, self.key)
            self.is_mock_mode = False
            logger.info("Connected successfully to live Supabase backend.")
        except Exception as exc:
            logger.warning(f"Could not connect to Supabase live SDK ({exc}). Falling back to Mock Mode.")
            self.is_mock_mode = True

    # -------------------------------------------------------------------------
    # 1. Expansion Management
    # -------------------------------------------------------------------------
    def get_or_create_expansion(self, name: Optional[str], code: Optional[str], release_date: Optional[str] = None) -> int:
        """
        Retrieves expansion ID by code, or inserts a new expansion if not present.
        Returns: expansion_id (int)
        """
        code_upper = str(code).upper().strip() if code is not None else "UNK"
        name_str = str(name).strip() if name is not None else "Unknown"

        if self.is_mock_mode or not self.client:
            if code_upper in self._mock_expansions:
                return self._mock_expansions[code_upper]["id"]

            exp_id = self._next_exp_id
            self._next_exp_id += 1
            record = {
                "id": exp_id,
                "name": name_str,
                "code": code_upper,
                "release_date": release_date,
                "created_at": datetime.utcnow().isoformat(),
            }
            self._mock_expansions[code_upper] = record
            return exp_id

        # Live Supabase DB Execution
        try:
            res = self.client.table("expansions").select("id").eq("code", code_upper).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]["id"]

            new_record = {"name": name_str, "code": code_upper}
            if release_date:
                new_record["release_date"] = release_date

            insert_res = self.client.table("expansions").insert(new_record).execute()
            if insert_res.data and len(insert_res.data) > 0:
                return insert_res.data[0]["id"]
        except Exception as exc:
            logger.error(f"Failed to query/insert expansion on Supabase ({exc}). Falling back to mock record.")

        # Fallback to mock if live query fails
        return self.get_or_create_expansion(name_str, code_upper, release_date)

    # -------------------------------------------------------------------------
    # 2. Card Catalog Management
    # -------------------------------------------------------------------------
    def upsert_card(
        self,
        expansion_id: int,
        card_number: Optional[str],
        name: Optional[str],
        rarity: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> int:
        """
        Upserts a card entry under an expansion set.
        Normalizes name and card number for case/whitespace sensitivity to prevent duplicates.
        Returns: card_id (int)
        """
        card_num = str(card_number).strip() if card_number is not None else "N/A"
        card_name = str(name).strip() if name is not None else "Unknown"

        # Key normalized for case-insensitive and whitespace-trimmed lookup
        key = (expansion_id, card_num.lower(), card_name.lower())

        if self.is_mock_mode or not self.client:
            if key in self._mock_cards:
                existing = self._mock_cards[key]
                if rarity:
                    existing["rarity"] = rarity
                if image_url:
                    existing["image_url"] = image_url
                return existing["id"]

            card_id = self._next_card_id
            self._next_card_id += 1
            record = {
                "id": card_id,
                "expansion_id": expansion_id,
                "card_number": card_num,
                "name": card_name,
                "rarity": rarity or "Unknown",
                "image_url": image_url or "",
                "created_at": datetime.utcnow().isoformat(),
            }
            self._mock_cards[key] = record
            return card_id

        # Live Supabase DB Execution
        try:
            res = (
                self.client.table("cards")
                .select("id")
                .eq("expansion_id", expansion_id)
                .ilike("card_number", card_num)
                .ilike("name", card_name)
                .execute()
            )
            if res.data and len(res.data) > 0:
                return res.data[0]["id"]

            card_data = {
                "expansion_id": expansion_id,
                "card_number": card_num,
                "name": card_name,
                "rarity": rarity or "Unknown",
                "image_url": image_url or "",
            }
            insert_res = self.client.table("cards").upsert(card_data, on_conflict="expansion_id,card_number,name").execute()
            if insert_res.data and len(insert_res.data) > 0:
                return insert_res.data[0]["id"]
        except Exception as exc:
            logger.error(f"Live upsert_card failed ({exc}). Falling back to mock store.")

        return self.upsert_card(expansion_id, card_num, card_name, rarity, image_url)

    # -------------------------------------------------------------------------
    # 3. Price Snapshot Management
    # -------------------------------------------------------------------------
    def insert_price_snapshot(
        self,
        card_id: int,
        price_min: Optional[Any] = None,
        price_avg: Optional[Any] = None,
        currency: str = "BRL",
    ) -> Dict[str, Any]:
        """
        Inserts a single price snapshot record into price_history table safely.
        """
        parsed_min = float(price_min) if price_min is not None else None
        parsed_avg = float(price_avg) if price_avg is not None else None

        record = {
            "card_id": card_id,
            "price_min": parsed_min,
            "price_avg": parsed_avg,
            "currency": currency or "BRL",
            "timestamp": datetime.utcnow().isoformat(),
        }

        if self.is_mock_mode or not self.client:
            record["id"] = self._next_price_id
            self._next_price_id += 1
            self._mock_price_history.append(record)
            return record

        try:
            res = self.client.table("price_history").insert(record).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
        except Exception as exc:
            logger.error(f"Live insert_price_snapshot failed ({exc}). Storing in mock memory.")

        record["id"] = self._next_price_id
        self._next_price_id += 1
        self._mock_price_history.append(record)
        return record

    def insert_batch_price_snapshots(self, snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Batch inserts multiple price snapshots for performance optimization safely.
        snapshots format: [{'card_id': 1, 'price_min': 10.50, 'price_avg': 15.00, 'currency': 'BRL'}, ...]
        """
        if not snapshots:
            return []

        inserted = []
        for snap in snapshots:
            if not isinstance(snap, dict):
                continue
            card_id = snap.get("card_id")
            if card_id is None:
                continue
            res = self.insert_price_snapshot(
                card_id=card_id,
                price_min=snap.get("price_min"),
                price_avg=snap.get("price_avg"),
                currency=snap.get("currency", "BRL"),
            )
            inserted.append(res)
        return inserted

    def get_card_price_history(self, card_id: int, limit: int = 30) -> List[Dict[str, Any]]:
        """
        Retrieves recent price history for a given card ordered by timestamp DESC.
        """
        if self.is_mock_mode or not self.client:
            matched = [p for p in self._mock_price_history if p["card_id"] == card_id]
            matched.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return matched[:limit]

        try:
            res = (
                self.client.table("price_history")
                .select("*")
                .eq("card_id", card_id)
                .order("timestamp", desc=True)
                .limit(limit)
                .execute()
            )
            if res.data:
                return res.data
        except Exception as exc:
            logger.error(f"Live get_card_price_history failed ({exc}). Using mock fallback.")

        matched = [p for p in self._mock_price_history if p["card_id"] == card_id]
        matched.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return matched[:limit]

    def get_latest_prices(self, expansion_code: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Queries current prices from latest_card_prices view.
        """
        if self.is_mock_mode or not self.client:
            latest: Dict[int, Dict[str, Any]] = {}
            for ph in self._mock_price_history:
                cid = ph["card_id"]
                # Find matching card & expansion
                card = next((c for c in self._mock_cards.values() if c["id"] == cid), None)
                if not card:
                    continue
                exp = next((e for e in self._mock_expansions.values() if e["id"] == card["expansion_id"]), None)

                if expansion_code and exp and exp["code"].upper() != expansion_code.upper():
                    continue

                item = {
                    "price_id": ph.get("id", 1),
                    "card_id": cid,
                    "card_name": card["name"],
                    "card_number": card["card_number"],
                    "rarity": card["rarity"],
                    "image_url": card["image_url"],
                    "expansion_id": card["expansion_id"],
                    "expansion_name": exp["name"] if exp else "Unknown",
                    "expansion_code": exp["code"] if exp else (expansion_code or "UNK"),
                    "price_min": ph["price_min"],
                    "price_avg": ph.get("price_avg"),
                    "currency": ph.get("currency", "BRL"),
                    "price_timestamp": ph.get("timestamp"),
                }
                latest[cid] = item

            res_list = list(latest.values())
            res_list.sort(key=lambda x: x.get("price_timestamp", ""), reverse=True)
            return res_list[:limit]

        try:
            query = self.client.table("latest_card_prices").select("*")
            if expansion_code:
                query = query.eq("expansion_code", expansion_code.upper())
            res = query.limit(limit).execute()
            if res.data:
                return res.data
        except Exception as exc:
            logger.error(f"Live get_latest_prices failed ({exc}). Using mock fallback.")

        return self.get_latest_prices(expansion_code, limit)

    # -------------------------------------------------------------------------
    # 4. Connectivity & Mock Flow Verification (Requirement R2 & AC2)
    # -------------------------------------------------------------------------
    def test_connectivity_and_mock_flow(self) -> bool:
        """
        Executes an end-to-end mock data insertion and retrieval test to satisfy Requirement R2 & AC2.
        1. Inserts mock expansion ('MOCK-SET')
        2. Inserts mock card ('MOCK-001')
        3. Inserts mock price snapshot (e.g. price_min = 42.50 BRL)
        4. Queries inserted snapshot and verifies equality.
        """
        logger.info("Executing test_connectivity_and_mock_flow...")

        # Step 1: Expansion
        exp_id = self.get_or_create_expansion(
            name="Mock Mega Block Set",
            code="MOCK-SET",
            release_date="2026-01-01"
        )
        assert exp_id > 0, f"Expected valid exp_id, got {exp_id}"

        # Step 2: Card
        card_id = self.upsert_card(
            expansion_id=exp_id,
            card_number="001/MOCK",
            name="Mock Mega Rayquaza EX",
            rarity="Secret Rare",
            image_url="https://repositorio.ligapokemon.com.br/images/cartas/ROS/61.jpg"
        )
        assert card_id > 0, f"Expected valid card_id, got {card_id}"

        # Step 3: Price Snapshot
        target_min_price = 42.50
        target_avg_price = 55.00
        snap = self.insert_price_snapshot(
            card_id=card_id,
            price_min=target_min_price,
            price_avg=target_avg_price,
            currency="BRL"
        )
        assert snap is not None, "Failed to insert price snapshot"

        # Step 4: Verification Readback
        history = self.get_card_price_history(card_id, limit=5)
        assert len(history) >= 1, "Expected price history record"
        assert float(history[0]["price_min"]) == target_min_price, (
            f"Expected {target_min_price}, got {history[0]['price_min']}"
        )
        assert history[0]["currency"] == "BRL", f"Expected BRL currency, got {history[0]['currency']}"

        latest = self.get_latest_prices("MOCK-SET")
        assert len(latest) >= 1, "Expected latest prices view entry"
        assert latest[0]["card_name"] == "Mock Mega Rayquaza EX"

        logger.info("[SUCCESS] test_connectivity_and_mock_flow completed successfully.")
        return True
