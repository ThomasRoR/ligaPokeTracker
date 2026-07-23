"""
HTML Parser Module.
Provides robust PT-BR currency parsing, HTML element extraction, and sample fixtures
for LigaPokemon card search listings across Mega Evolution block expansions.
"""

import re
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Fallback HTML Fixtures for Mega Evolution block cards when offline or running tests
SAMPLE_HTML_FIXTURES = {
    "ROS": """
    <div class="card-listing-container">
        <div class="item-card" data-id="1001">
            <div class="card-name"><a href="/?view=cards/card&card=M+Rayquaza+EX&ed=ROS" title="M Rayquaza EX">M Rayquaza EX</a></div>
            <div class="card-number">61/108</div>
            <div class="card-rarity" title="Ultra Rara">Ultra Rara</div>
            <div class="card-image"><img class="card-img" src="https://repositorio.ligapokemon.com.br/images/cartas/ROS/61.jpg" alt="M Rayquaza EX" /></div>
            <div class="price-box">
                <span class="preco-menor">R$ 145,90</span>
                <span class="preco-medio">R$ 180,00</span>
            </div>
        </div>
        <div class="item-card" data-id="1002">
            <div class="card-name"><a href="/?view=cards/card&card=M+Latios+EX&ed=ROS" title="M Latios EX">M Latios EX</a></div>
            <div class="card-number">59/108</div>
            <div class="card-rarity" title="Ultra Rara">Ultra Rara</div>
            <div class="card-image"><img class="card-img" src="https://repositorio.ligapokemon.com.br/images/cartas/ROS/59.jpg" alt="M Latios EX" /></div>
            <div class="price-box">
                <span class="preco-menor">R$ 42,50</span>
                <span class="preco-medio">R$ 55,00</span>
            </div>
        </div>
        <div class="item-card" data-id="1003">
            <div class="card-name"><a href="/?view=cards/card&card=Shaymin+EX&ed=ROS" title="Shaymin EX">Shaymin EX</a></div>
            <div class="card-number">77/108</div>
            <div class="card-rarity" title="Ultra Rara">Ultra Rara</div>
            <div class="card-image"><img class="card-img" src="https://repositorio.ligapokemon.com.br/images/cartas/ROS/77.jpg" alt="Shaymin EX" /></div>
            <div class="price-box">
                <span class="preco-menor">R$ 89,00</span>
                <span class="preco-medio">R$ 110,00</span>
            </div>
        </div>
    </div>
    """,
    "EVO": """
    <div class="card-listing-container">
        <div class="item-card" data-id="2001">
            <div class="card-name"><a href="/?view=cards/card&card=M+Charizard+EX&ed=EVO" title="M Charizard EX">M Charizard EX</a></div>
            <div class="card-number">13/108</div>
            <div class="card-rarity" title="Ultra Rara">Ultra Rara</div>
            <div class="card-image"><img class="card-img" src="https://repositorio.ligapokemon.com.br/images/cartas/EVO/13.jpg" alt="M Charizard EX" /></div>
            <div class="price-box">
                <span class="preco-menor">R$ 250,00</span>
                <span class="preco-medio">R$ 310,00</span>
            </div>
        </div>
        <div class="item-card" data-id="2002">
            <div class="card-name"><a href="/?view=cards/card&card=M+Blastoise+EX&ed=EVO" title="M Blastoise EX">M Blastoise EX</a></div>
            <div class="card-number">22/108</div>
            <div class="card-rarity" title="Ultra Rara">Ultra Rara</div>
            <div class="card-image"><img class="card-img" src="https://repositorio.ligapokemon.com.br/images/cartas/EVO/22.jpg" alt="M Blastoise EX" /></div>
            <div class="price-box">
                <span class="preco-menor">R$ 75,00</span>
                <span class="preco-medio">R$ 95,00</span>
            </div>
        </div>
    </div>
    """,
    "PRC": """
    <div class="card-listing-container">
        <div class="item-card" data-id="3001">
            <div class="card-name"><a href="/?view=cards/card&card=Primal+Kyogre+EX&ed=PRC" title="Primal Kyogre EX">Primal Kyogre EX</a></div>
            <div class="card-number">55/160</div>
            <div class="card-rarity" title="Ultra Rara">Ultra Rara</div>
            <div class="card-image"><img class="card-img" src="https://repositorio.ligapokemon.com.br/images/cartas/PRC/55.jpg" alt="Primal Kyogre EX" /></div>
            <div class="price-box">
                <span class="preco-menor">R$ 115,00</span>
                <span class="preco-medio">R$ 140,00</span>
            </div>
        </div>
        <div class="item-card" data-id="3002">
            <div class="card-name"><a href="/?view=cards/card&card=M+Gardevoir+EX&ed=PRC" title="M Gardevoir EX">M Gardevoir EX</a></div>
            <div class="card-number">106/160</div>
            <div class="card-rarity" title="Ultra Rara">Ultra Rara</div>
            <div class="card-image"><img class="card-img" src="https://repositorio.ligapokemon.com.br/images/cartas/PRC/106.jpg" alt="M Gardevoir EX" /></div>
            <div class="price-box">
                <span class="preco-menor">R$ 68,50</span>
                <span class="preco-medio">R$ 85,00</span>
            </div>
        </div>
    </div>
    """,
    "DEFAULT": """
    <div class="card-listing-container">
        <div class="item-card" data-id="9001">
            <div class="card-name"><a href="/?view=cards/card&card=M+Lucario+EX&ed=PRC" title="M Lucario EX">M Lucario EX</a></div>
            <div class="card-number">55/111</div>
            <div class="card-rarity" title="Ultra Rara">Ultra Rara</div>
            <div class="card-image"><img class="card-img" src="https://repositorio.ligapokemon.com.br/images/cartas/PRC/55.jpg" alt="M Lucario EX" /></div>
            <div class="price-box">
                <span class="preco-menor">R$ 1.234,56</span>
                <span class="preco-medio">R$ 1.500,00</span>
            </div>
        </div>
    </div>
    """
}


def clean_currency(price_str: Any) -> Optional[float]:
    """
    Sanitizes Brazilian Real (PT-BR) currency string formats into standard float.
    Handles ints, floats, PT-BR format ('R$ 1.234,56'), dot-decimal ('12.50'),
    negative values ('-10,00'), and invalid inputs gracefully.
    """
    if price_str is None or isinstance(price_str, bool):
        return None

    if isinstance(price_str, (int, float)):
        return float(price_str)

    if not isinstance(price_str, str):
        return None

    # Clean whitespace, non-breaking spaces, and currency symbols
    cleaned = (
        price_str
        .replace("&nbsp;", "")
        .replace("\xa0", "")
        .replace("R$", "")
        .replace("BRL", "")
        .strip()
    )

    if not cleaned or cleaned in ("-", "N/A", "null", "none", "--"):
        return None

    # Determine if negative or positive
    is_negative = False
    if cleaned.startswith("-"):
        is_negative = True
        cleaned = cleaned[1:].strip()
    elif cleaned.startswith("+"):
        cleaned = cleaned[1:].strip()

    # Handle range strings if present (e.g., '10,00 - 15,00' -> take first '10,00')
    if "-" in cleaned:
        parts = [p.strip() for p in cleaned.split("-") if p.strip()]
        if parts:
            cleaned = parts[0]

    # Extract numeric token (digits, dots, commas)
    match = re.search(r'(\d+(?:[\.,]\d+)*)', cleaned)
    if not match:
        return None

    num_str = match.group(1)

    has_dot = "." in num_str
    has_comma = "," in num_str

    if has_dot and has_comma:
        dot_idx = num_str.find(".")
        comma_idx = num_str.find(",")
        if dot_idx < comma_idx:
            # PT-BR format: 1.234,56 -> remove dots, swap comma to dot
            num_str = num_str.replace(".", "").replace(",", ".")
        else:
            # US format: 1,234.56 -> remove commas
            num_str = num_str.replace(",", "")
    elif has_comma:
        if num_str.count(",") > 1:
            return None
        num_str = num_str.replace(",", ".")
    elif has_dot:
        if num_str.count(".") > 1:
            parts = num_str.split(".")
            if len(parts[-1]) == 3 and all(len(p) == 3 for p in parts[1:-1]):
                num_str = "".join(parts)
            else:
                return None
        else:
            # Single dot (e.g. 12.50 or 1234.56) -> keep dot
            pass

    try:
        val = float(num_str)
        return -val if is_negative else val
    except ValueError:
        return None


def parse_cards_from_html(html_content: str, expansion_code: str = "") -> List[Dict[str, Any]]:
    """
    Parses HTML content from LigaPokemon search/listing pages.
    Returns a list of extracted card metadata dictionaries.
    """
    cards: List[Dict[str, Any]] = []
    if not html_content or not html_content.strip():
        return cards

    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Look for card containers using standard CSS selectors
        card_items = (
            soup.select(".item-card") or 
            soup.select("tr.linha-carta") or 
            soup.select("div.carta") or 
            soup.select(".card-item")
        )

        for item in card_items:
            # 1. Card Name
            name_el = (
                item.select_one(".card-name a") or 
                item.select_one(".card-name") or 
                item.select_one(".nome-carta") or 
                item.select_one("td.nome a")
            )
            card_name = name_el.get_text(strip=True) if name_el else ""
            if not card_name and name_el and name_el.has_attr("title"):
                card_name = name_el["title"].strip()

            if card_name:
                import html as html_lib
                card_name = html_lib.unescape(card_name)

            # 2. Card Number
            number_el = (
                item.select_one(".card-number") or 
                item.select_one(".num-carta") or 
                item.select_one("span.numero")
            )
            card_number = number_el.get_text(strip=True) if number_el else ""
            if not card_number:
                # Regex search inside element text for number patterns (e.g., 61/108)
                match = re.search(r"\b\d+/\d+\b", item.get_text())
                if match:
                    card_number = match.group(0)

            # 3. Rarity
            rarity_el = (
                item.select_one(".card-rarity") or 
                item.select_one(".raridade") or 
                item.select_one("img[title*='Rara']")
            )
            rarity = ""
            if rarity_el:
                rarity = rarity_el.get("title", "") or rarity_el.get_text(strip=True)

            # 4. Image URL
            img_el = (
                item.select_one("img.card-img") or 
                item.select_one("img.carta-img") or 
                item.select_one("img[src*='cartas']")
            )
            image_url = ""
            if img_el and img_el.has_attr("src"):
                image_url = img_el["src"]
                if image_url.startswith("//"):
                    image_url = "https:" + image_url

            # 5. Price Min & Avg
            price_min_el = (
                item.select_one(".preco-menor") or 
                item.select_one(".price-min") or 
                item.select_one(".preco-minimo")
            )
            price_avg_el = (
                item.select_one(".preco-medio") or 
                item.select_one(".price-avg") or 
                item.select_one(".preco-mediano")
            )

            raw_price_min = price_min_el.get_text(strip=True) if price_min_el else None
            raw_price_avg = price_avg_el.get_text(strip=True) if price_avg_el else None

            price_min = clean_currency(raw_price_min)
            price_avg = clean_currency(raw_price_avg)

            if card_name and (card_number or price_min is not None):
                cards.append({
                    "name": card_name,
                    "card_number": card_number or "N/A",
                    "expansion_code": expansion_code,
                    "rarity": rarity or "Unknown",
                    "image_url": image_url,
                    "price_min": price_min if price_min is not None else 0.0,
                    "price_avg": price_avg,
                    "currency": "BRL",
                })

    except ImportError:
        logger.warning("BeautifulSoup4 not available. Using regex fallback parser.")
        cards = _regex_fallback_parser(html_content, expansion_code)

    # Fallback to regex if BS4 parsed 0 cards from non-empty html
    if not cards and html_content:
        cards = _regex_fallback_parser(html_content, expansion_code)

    return cards


def _regex_fallback_parser(html_content: str, expansion_code: str = "") -> List[Dict[str, Any]]:
    """Defensive regex fallback parser for card extraction across diverse HTML DOM structures."""
    cards: List[Dict[str, Any]] = []
    if not html_content or not html_content.strip():
        return cards

    # Find start indices of item card blocks using common class patterns
    card_start_pattern = r'<(?:div|tr|li)[^>]*class="[^"]*(?:item-card|linha-carta|carta|card-item)[^"]*"[^>]*>'
    matches = list(re.finditer(card_start_pattern, html_content, re.IGNORECASE))

    if matches:
        blocks = []
        for i in range(len(matches)):
            start_idx = matches[i].start()
            end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(html_content)
            blocks.append(html_content[start_idx:end_idx])
    else:
        name_matches = list(re.finditer(r'class="[^"]*card-name[^"]*"', html_content, re.IGNORECASE))
        if len(name_matches) > 1:
            blocks = []
            for i in range(len(name_matches)):
                start_idx = name_matches[i].start()
                end_idx = name_matches[i + 1].start() if i + 1 < len(name_matches) else len(html_content)
                blocks.append(html_content[start_idx:end_idx])
        else:
            blocks = [html_content]

    for block in blocks:
        # Match card name
        name_match = (
            re.search(r'class="[^"]*card-name[^"]*"[^>]*>(?:\s*<a[^>]*?(?:title="([^"]+)")?[^>]*>)?([^<]*)', block, re.IGNORECASE) or
            re.search(r'<a[^>]*href="[^"]*card=([^"&]+)', block, re.IGNORECASE) or
            re.search(r'class="[^"]*nome-carta[^"]*"[^>]*>(?:\s*<a[^>]*>)?([^<]*)', block, re.IGNORECASE) or
            re.search(r'title="([^"]+)"', block)
        )

        card_name = ""
        if name_match:
            g1 = name_match.group(1) if name_match.lastindex and name_match.lastindex >= 1 else None
            g2 = name_match.group(2) if name_match.lastindex and name_match.lastindex >= 2 else None
            card_name = (g1 or g2 or "").strip()
            import html as html_lib
            card_name = html_lib.unescape(card_name)

        if not card_name:
            continue

        # Match number
        num_match = re.search(r'class="[^"]*card-number[^"]*"[^>]*>([^<]+)</div>', block, re.IGNORECASE) or re.search(r'\b(\d+/\d+)\b', block)
        card_number = num_match.group(1).strip() if num_match else ""

        # Match prices
        price_min_match = re.search(r'class="[^"]*(?:preco-menor|price-min|preco-minimo)[^"]*"[^>]*>([^<]+)</span>', block, re.IGNORECASE)
        price_avg_match = re.search(r'class="[^"]*(?:preco-medio|price-avg|preco-mediano)[^"]*"[^>]*>([^<]+)</span>', block, re.IGNORECASE)

        raw_price_min = price_min_match.group(1) if price_min_match else None
        raw_price_avg = price_avg_match.group(1) if price_avg_match else None

        if not raw_price_min:
            prices = re.findall(r'R\$\s*[\d\.,]+', block)
            if prices:
                raw_price_min = prices[0]
                if len(prices) > 1:
                    raw_price_avg = prices[1]

        price_min = clean_currency(raw_price_min)
        price_avg = clean_currency(raw_price_avg)

        if not card_number and price_min is None:
            continue

        # Match image
        img_match = re.search(r'src="([^"]+)"', block)
        image_url = img_match.group(1) if img_match else ""
        if image_url.startswith("//"):
            image_url = "https:" + image_url

        cards.append({
            "name": card_name,
            "card_number": card_number or "N/A",
            "expansion_code": expansion_code,
            "rarity": "Ultra Rara",
            "image_url": image_url,
            "price_min": price_min if price_min is not None else 0.0,
            "price_avg": price_avg,
            "currency": "BRL",
        })

    return cards
