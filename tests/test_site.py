"""Regression tests for the frozen research website."""

from __future__ import annotations

import json
import re
from pathlib import Path

from website.app import create_app
from website.data_loader import DataLoader


def test_home_has_semantic_hero_and_entity_identity() -> None:
    app = create_app("production")
    response = app.test_client().get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'data-research-field' in html
    assert '<canvas id="hero-canvas" aria-hidden="true"></canvas>' in html
    assert 'Building intelligence for the physical world.' in html
    assert 'https://anuroopsriram.com/#person' in html
    assert 'googletagmanager.com/gtag/js' in html


def test_development_does_not_emit_analytics() -> None:
    app = create_app("development")
    html = app.test_client().get("/").get_data(as_text=True)
    assert "googletagmanager.com/gtag/js" not in html


def test_publication_index_is_searchable_and_semantic() -> None:
    app = create_app("production")
    html = app.test_client().get("/publications/").get_data(as_text=True)

    assert '<search class="pub-search"' in html
    assert 'aria-pressed="true"' in html
    assert '<article class="pub-card' in html
    assert ' popover>' in html


def test_every_publication_has_detail_and_citation_routes() -> None:
    app = create_app("production")
    client = app.test_client()

    for publication in DataLoader().load_yaml_file("publist.yml"):
        key = publication["key"]
        detail = client.get(f"/publications/{key}/")
        bibtex = client.get(f"/publications/{key}/citation.bib")
        ris = client.get(f"/publications/{key}/citation.ris")

        assert detail.status_code == 200
        assert publication["title"] in detail.get_data(as_text=True)
        assert f"/publications/{key}/" in detail.get_data(as_text=True)
        assert bibtex.status_code == 200
        assert bibtex.get_data(as_text=True).startswith("@article{")
        assert ris.status_code == 200
        assert ris.get_data(as_text=True).startswith("TY  - JOUR")


def test_publication_jsonld_uses_canonical_on_domain_id() -> None:
    publication = DataLoader().load_yaml_file("publist.yml")[0]
    app = create_app("production")
    html = (
        app.test_client()
        .get(f"/publications/{publication['key']}/")
        .get_data(as_text=True)
    )
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL
    )
    objects = [json.loads(block) for block in blocks]
    article = next(obj for obj in objects if obj.get("@type") == "ScholarlyArticle")

    assert article["@id"].startswith("https://anuroopsriram.com/publications/")
    assert article["creator"]["@id"] == "https://anuroopsriram.com/#person"


def test_sitemap_and_feed_expose_deep_links() -> None:
    publication = DataLoader().load_yaml_file("publist.yml")[0]
    app = create_app("production")
    client = app.test_client()
    sitemap = client.get("/sitemap.xml").get_data(as_text=True)
    feed = client.get("/feed.xml").get_data(as_text=True)

    assert "https://anuroopsriram.com/feed.xml" in sitemap
    assert f"https://anuroopsriram.com/publications/{publication['key']}/" in sitemap
    assert re.search(
        r"https://anuroopsriram\.com/allnews/#news-\d{4}-\d{2}-\d+", feed
    )


def test_graphics_have_complete_fallback_contract() -> None:
    with open("static/js/research-field.js", encoding="utf-8") as field_file:
        field_source = field_file.read()
    with open("static/css/_vision.scss", encoding="utf-8") as css_file:
        css_source = css_file.read()

    assert "navigator.gpu" in field_source
    assert "loadWebGLFallback" in field_source
    assert "prefers-reduced-motion" in field_source
    assert ".home-hero.hero-fallback" in css_source


def test_frontend_payload_and_loading_budgets() -> None:
    """Keep the first navigation small and GPU work out of the critical path."""
    app = create_app("production")
    html = app.test_client().get("/").get_data(as_text=True)
    css_size = Path("static/css/main.css").stat().st_size
    critical_css_size = Path("static/css/critical.css").stat().st_size
    field_size = Path("static/js/research-field.js").stat().st_size
    font_size = sum(path.stat().st_size for path in Path("static/fonts").glob("*.woff2"))

    assert css_size < 80_000
    assert critical_css_size < 12_000
    assert field_size < 20_000
    assert font_size < 250_000
    assert '<script type="module" src="/static/js/research-field.js">' in html
    assert 'href="/static/css/main.css" media="print"' in html
    assert html.index("/static/js/research-field.js") > html.index('id="hero-canvas"')
