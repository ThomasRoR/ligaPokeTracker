"""
Data Models Module.
Provides dataclass models for Expansions, Cards, and Price Snapshots.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Expansion:
    """Represents a Pokémon TCG expansion set."""

    code: str
    name: str
    name_pt: Optional[str] = None
    slug: Optional[str] = None
    release_date: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "name": self.name,
            "code": self.code,
        }
        if self.release_date:
            data["release_date"] = self.release_date
        if self.id is not None:
            data["id"] = self.id
        return data


@dataclass
class Card:
    """Represents an individual Pokémon card entry."""

    card_number: str
    name: str
    expansion_code: str
    expansion_id: Optional[int] = None
    rarity: Optional[str] = None
    image_url: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "card_number": self.card_number,
            "name": self.name,
        }
        if self.expansion_id is not None:
            data["expansion_id"] = self.expansion_id
        if self.rarity:
            data["rarity"] = self.rarity
        if self.image_url:
            data["image_url"] = self.image_url
        if self.id is not None:
            data["id"] = self.id
        return data


@dataclass
class PriceSnapshot:
    """Represents a historical price record for a card at a given timestamp."""

    price_min: float
    card_id: Optional[int] = None
    price_avg: Optional[float] = None
    currency: str = "BRL"
    timestamp: Optional[str] = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    id: Optional[int] = None
    # Auxiliary fields for offline reporting/tracking
    card_number: Optional[str] = None
    card_name: Optional[str] = None
    expansion_code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "price_min": self.price_min,
            "currency": self.currency,
        }
        if self.card_id is not None:
            data["card_id"] = self.card_id
        if self.price_avg is not None:
            data["price_avg"] = self.price_avg
        if self.timestamp:
            data["timestamp"] = self.timestamp
        if self.id is not None:
            data["id"] = self.id
        return data
