"""
Scraper Configuration Module.
Defines Mega Evolution block expansions metadata, network request parameters, and HTML DOM selectors.
"""

# Base URL for LigaPokemon platform
BASE_URL = "https://www.ligapokemon.com.br/"
SEARCH_ENDPOINT = "https://www.ligapokemon.com.br/?view=cards/search"

# 8 Target Mega Evolution Block Expansions (XY Series)
MEGA_EVOLUTION_EXPANSIONS = [
    {
        "code": "PBL",
        "slug": "Copag-Poderes-de-Batalha",
        "name": "Coleção Poderes de Batalha",
        "name_pt": "Poderes de Batalha",
        "release_date": "2016-01-01",
    },
    {
        "code": "ASC",
        "slug": "Copag-Ascensao",
        "name": "Coleção Ascensão",
        "name_pt": "Ascensão",
        "release_date": "2016-01-01",
    },
    {
        "code": "POR",
        "slug": "Copag-Portais",
        "name": "Coleção Portais",
        "name_pt": "Portais",
        "release_date": "2016-01-01",
    },
    {
        "code": "CRI",
        "slug": "Copag-Criadores",
        "name": "Coleção Criadores",
        "name_pt": "Criadores",
        "release_date": "2016-01-01",
    },
    {
        "code": "MEG",
        "slug": "Copag-Mega-Evolucao",
        "name": "Coleção Mega Evolução",
        "name_pt": "Mega Evolução",
        "release_date": "2016-01-01",
    },
    {
        "code": "MEP",
        "slug": "Copag-Mega-Poderes",
        "name": "Coleção Mega Poderes",
        "name_pt": "Mega Poderes",
        "release_date": "2016-01-01",
    },
    {
        "code": "PFL",
        "slug": "Copag-Poderes-de-Fogo-Luz",
        "name": "Coleção Poderes de Fogo e Luz",
        "name_pt": "Poder de Fogo e Luz",
        "release_date": "2016-01-01",
    }
]

# Lookup map by set code
EXPANSIONS_BY_CODE = {item["code"]: item for item in MEGA_EVOLUTION_EXPANSIONS}

# Standard browser headers to avoid anti-bot blocks
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": BASE_URL,
}

# Request configuration parameters
REQUEST_TIMEOUT_SECONDS = 10
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.5
REQUEST_DELAY_SECONDS = 1.0

# DOM Selectors map for LigaPokemon web page elements
DOM_SELECTORS = {
    "card_container": [".item-card", ".card-item", "tr.linha-carta", "div.carta", ".card-listing"],
    "card_name": [".card-name", ".nome-carta", "td.nome a", "a.card-title", ".name"],
    "card_number": [".card-number", ".num-carta", "span.numero", ".collector-number"],
    "rarity": [".card-rarity", ".raridade", "img[title*='Rara']", ".rarity-icon"],
    "image_url": ["img.card-img", "img.carta-img", "img[src*='cartas']", "img.art"],
    "price_min": [".preco-menor", ".price-min", ".preco-minimo", "span.price-val"],
    "price_avg": [".preco-medio", ".price-avg", ".preco-mediano"],
}
