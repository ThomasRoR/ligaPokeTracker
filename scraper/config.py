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
        "code": "PRC",
        "slug": "XY-Crise-Primordial",
        "name": "XY - Primal Clash",
        "name_pt": "XY - Crise Primordial",
        "release_date": "2015-02-04",
    },
    {
        "code": "ROS",
        "slug": "XY-Furia-dos-Ceus",
        "name": "XY - Roaring Skies",
        "name_pt": "XY - Fúria dos Céus",
        "release_date": "2015-05-06",
    },
    {
        "code": "AOR",
        "slug": "XY-Origens-Seculares",
        "name": "XY - Ancient Origins",
        "name_pt": "XY - Origens Seculares",
        "release_date": "2015-08-12",
    },
    {
        "code": "BKT",
        "slug": "XY-Turbo-Revolucao",
        "name": "XY - BREAKthrough",
        "name_pt": "XY - Turbo Revolução",
        "release_date": "2015-11-04",
    },
    {
        "code": "BKP",
        "slug": "XY-Turbo-Colisao",
        "name": "XY - BREAKpoint",
        "name_pt": "XY - Turbo Colisão",
        "release_date": "2016-02-03",
    },
    {
        "code": "FCO",
        "slug": "XY-Fusao-de-Destinos",
        "name": "XY - Fates Collide",
        "name_pt": "XY - Fusão de Destinos",
        "release_date": "2016-05-02",
    },
    {
        "code": "STS",
        "slug": "XY-Cerco-do-Vapor",
        "name": "XY - Steam Siege",
        "name_pt": "XY - Cerco do Vapor",
        "release_date": "2016-08-03",
    },
    {
        "code": "EVO",
        "slug": "XY-Evolucoes",
        "name": "XY - Evolutions",
        "name_pt": "XY - Evoluções",
        "release_date": "2016-11-02",
    },
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
