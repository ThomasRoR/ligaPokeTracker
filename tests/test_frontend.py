"""
Front-End Test Suite for Pokémon Price Tracker - Milestone 3.
Verifies static web front-end structure, HTML validity, JS query & mock fallback logic,
and local HTTP static serving via http.server.
"""

import os
import re
import socket
import threading
import unittest
import urllib.request
import urllib.error
from functools import partial
from http.server import SimpleHTTPRequestHandler, HTTPServer
from html.parser import HTMLParser

# Project Root & Frontend Directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")


class HTMLValidator(HTMLParser):
  """Simple HTML DOM Structure Parser & Validator."""

  def __init__(self):
    super().__init__()
    self.title_text = ""
    self.in_title = False
    self.inputs = []
    self.selects = []
    self.options = []
    self.scripts = []
    self.links = []
    self.div_ids = []
    self.div_classes = []

  def handle_starttag(self, tag, attrs):
    attr_dict = dict(attrs)

    if tag == "title":
      self.in_title = True
    elif tag == "input":
      self.inputs.append(attr_dict)
    elif tag == "select":
      self.selects.append(attr_dict)
    elif tag == "option":
      self.options.append(attr_dict)
    elif tag == "script":
      self.scripts.append(attr_dict)
    elif tag == "link":
      self.links.append(attr_dict)

    if "id" in attr_dict:
      self.div_ids.append(attr_dict["id"])
    if "class" in attr_dict:
      self.div_classes.extend(attr_dict["class"].split())

  def handle_endtag(self, tag):
    if tag == "title":
      self.in_title = False

  def handle_data(self, data):
    if self.in_title:
      self.title_text += data


class TestFrontendSuite(unittest.TestCase):
  """Unit and Integration Tests for static front-end assets & HTTP serving."""

  def setUp(self):
    self.index_path = os.path.join(FRONTEND_DIR, "index.html")
    self.styles_path = os.path.join(FRONTEND_DIR, "styles.css")
    self.client_path = os.path.join(FRONTEND_DIR, "supabaseClient.js")
    self.app_path = os.path.join(FRONTEND_DIR, "app.js")

  def test_1_frontend_files_exist(self):
    """Verifies that all required front-end asset files exist in frontend/ directory."""
    self.assertTrue(
        os.path.isdir(FRONTEND_DIR), f"Directory missing: {FRONTEND_DIR}"
    )
    self.assertTrue(
        os.path.isfile(self.index_path),
        f"File missing: {self.index_path}",
    )
    self.assertTrue(
        os.path.isfile(self.styles_path),
        f"File missing: {self.styles_path}",
    )
    self.assertTrue(
        os.path.isfile(self.client_path),
        f"File missing: {self.client_path}",
    )
    self.assertTrue(
        os.path.isfile(self.app_path),
        f"File missing: {self.app_path}",
    )

  def test_2_index_html_structure_and_syntax(self):
    """Verifies HTML5 syntax, page title, search bar, expansion filter dropdown, cards grid, modal, and script tags."""
    with open(self.index_path, "r", encoding="utf-8") as f:
      html_content = f.read()

    # 1. Doctype check
    self.assertTrue(
        html_content.strip().lower().startswith("<!doctype html>"),
        "index.html must start with HTML5 <!DOCTYPE html>",
    )

    parser = HTMLValidator()
    parser.feed(html_content)

    # 2. Page title
    expected_title = "Pokémon Price Tracker - Mega Evolution Block"
    self.assertIn(
        expected_title,
        parser.title_text,
        f"Title '{parser.title_text}' does not contain expected '{expected_title}'",
    )

    # 3. Search Bar Input
    search_inputs = [
        inp for inp in parser.inputs if inp.get("id") == "card-search"
    ]
    self.assertTrue(
        len(search_inputs) > 0,
        "index.html missing search input with id='card-search'",
    )

    # 4. Expansion Select Dropdown
    exp_selects = [
        sel for sel in parser.selects if sel.get("id") == "expansion-filter"
    ]
    self.assertTrue(
        len(exp_selects) > 0,
        "index.html missing expansion filter select with id='expansion-filter'",
    )

    # Options verify 8 Mega Evolution sets or All
    target_expansions = [
        "XY - Primal Clash",
        "XY - Roaring Skies",
        "XY - Ancient Origins",
        "XY - BREAKthrough",
        "XY - BREAKpoint",
        "XY - Fates Collide",
        "XY - Steam Siege",
        "XY - Evolutions",
    ]
    for target in target_expansions:
      self.assertIn(
          target,
          html_content,
          f"index.html missing expansion dropdown option for '{target}'",
      )

    # 5. Cards Grid Container
    self.assertIn(
        "cards-grid",
        parser.div_ids + parser.div_classes,
        "index.html missing cards grid container with id/class 'cards-grid'",
    )

    # 6. Price History Modal
    self.assertIn(
        "price-history-modal",
        parser.div_ids,
        "index.html missing modal container with id='price-history-modal'",
    )

    # 7. Script tags for Supabase CDN, supabaseClient.js, app.js
    script_sources = [s.get("src", "") for s in parser.scripts if "src" in s]
    self.assertTrue(
        any("@supabase/supabase-js" in src for src in script_sources),
        "index.html missing CDN script tag for @supabase/supabase-js",
    )
    self.assertTrue(
        any("supabaseClient.js" in src for src in script_sources),
        "index.html missing script tag for supabaseClient.js",
    )
    self.assertTrue(
        any("app.js" in src for src in script_sources),
        "index.html missing script tag for app.js",
    )

  def test_3_javascript_supabase_query_and_mock_fallback(self):
    """Verifies JS logic for Supabase API direct queries (latest_card_prices view) and offline mock dataset."""
    with open(self.client_path, "r", encoding="utf-8") as f:
      client_code = f.read()

    with open(self.app_path, "r", encoding="utf-8") as f:
      app_code = f.read()

    # Verify Supabase client instantiation / createClient call
    self.assertIn(
        "createClient",
        client_code,
        "supabaseClient.js missing createClient call for Supabase JS library",
    )

    # Verify Database View / Tables queries
    self.assertTrue(
        "latest_card_prices" in client_code or "cards" in client_code,
        "supabaseClient.js must query latest_card_prices view or cards table",
    )
    self.assertIn(
        "price_history",
        client_code,
        "supabaseClient.js must query price_history table for time-series snapshots",
    )
    self.assertIn(
        "expansions",
        client_code,
        "supabaseClient.js must query expansions table",
    )

    # Verify Mock Data Fallback contains 8 Mega Evolution sets
    mock_codes = ["PRC", "ROS", "AOR", "BKT", "BKP", "FCO", "STS", "EVO"]
    for code in mock_codes:
      self.assertIn(
          code,
          client_code,
          f"supabaseClient.js mock dataset missing expansion code '{code}'",
      )

    # Verify App functions in app.js
    required_functions = [
        "loadExpansions",
        "loadCards",
        "filterCards",
        "showPriceHistoryModal",
    ]
    for func in required_functions:
      self.assertIn(
          func,
          app_code,
          f"app.js missing required application function '{func}'",
      )

  def test_4_local_static_http_server_serving(self):
    """Launches http.server on local port, fetches static files, and asserts HTTP 200 responses."""

    # Find free local port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    handler = partial(SimpleHTTPRequestHandler, directory=FRONTEND_DIR)
    server = HTTPServer(("127.0.0.1", port), handler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
      base_url = f"http://127.0.0.1:{port}"
      endpoints = [
          "/index.html",
          "/styles.css",
          "/supabaseClient.js",
          "/app.js",
      ]

      for ep in endpoints:
        url = base_url + ep
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
          self.assertEqual(
              resp.status,
              200,
              f"Endpoint {ep} returned status code {resp.status}, expected 200",
          )
          content = resp.read().decode("utf-8")
          self.assertTrue(
              len(content) > 0,
              f"Endpoint {ep} returned empty response body",
          )

    finally:
      server.shutdown()
      server.server_close()
      server_thread.join(timeout=2)


if __name__ == "__main__":
  unittest.main()
