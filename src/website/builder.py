"""Shared build logic for the website."""

from __future__ import annotations

import os
import re
import shutil
from collections.abc import Iterator
from pathlib import Path

from flask_frozen import Freezer

from .app import create_app
from .data_loader import DataLoader

DEFAULT_OUTPUT_DIR = "docs"
CSS_SOURCES = (
    "static/css/main.scss",
    "static/css/_home.scss",
    "static/css/_pages.scss",
    "static/css/_motion.scss",
    "static/css/_vision.scss",
)
CRITICAL_CSS_SOURCE = "static/css/critical.scss"


def log(message: str, use_click: bool = False) -> None:
    if use_click:
        import click

        click.echo(message)
    else:
        print(message)


def _compact_css(css: str) -> str:
    """Remove comments and formatting while preserving CSS token boundaries."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    return "\n".join(line.strip() for line in css.splitlines() if line.strip()) + "\n"


def compile_css(use_click: bool = False) -> None:
    """Bundle native CSS and emit a small home-page critical stylesheet."""
    log("Bundling native CSS...", use_click)
    os.makedirs("static/css", exist_ok=True)
    chunks = []
    for source in CSS_SOURCES:
        with open(source, encoding="utf-8") as css_file:
            chunks.append(css_file.read())
            chunks.append("\n")
    with open("static/css/main.css", "w", encoding="utf-8") as css_file:
        css_file.write(_compact_css("".join(chunks)))
    with open(CRITICAL_CSS_SOURCE, encoding="utf-8") as critical_file:
        critical_css = _compact_css(critical_file.read())
    with open("static/css/critical.css", "w", encoding="utf-8") as css_file:
        css_file.write(critical_css)
    log("Native CSS bundle complete.", use_click)


def copy_static_files(use_click: bool = False) -> None:
    """Copy static files to the static directory."""
    log("Copying static files...", use_click)

    os.makedirs("static/images", exist_ok=True)
    os.makedirs("static/fonts", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)

    for src_dir, dst_dir in [
        ("images", "static/images"),
        ("fonts", "static/fonts"),
        ("js", "static/js"),
    ]:
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

    if os.path.exists("CNAME"):
        shutil.copy2("CNAME", "static/")

    log("Static files copied.", use_click)


def build_site(output_dir: str | None = None, use_click: bool = False) -> None:
    """Build the static site."""
    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..", DEFAULT_OUTPUT_DIR
        )
        output_dir = os.path.normpath(output_dir)

    log("Building static site...", use_click)

    app = create_app("production")
    app.config["FREEZER_DESTINATION"] = output_dir
    app.config["FREEZER_RELATIVE_URLS"] = True
    app.config["FREEZER_IGNORE_404_NOT_FOUND"] = True
    freezer = Freezer(app)

    @freezer.register_generator  # type: ignore[misc]
    def publication_routes() -> Iterator[tuple[str, dict[str, str]]]:
        for publication in DataLoader().load_yaml_file("publist.yml"):
            key = publication.get("key")
            if not key:
                continue
            yield "main.publication_detail", {"key": key}
            yield "main.publication_bibtex", {"key": key}
            yield "main.publication_ris", {"key": key}

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    compile_css(use_click)
    copy_static_files(use_click)
    freezer.freeze()

    if os.path.exists("static"):
        shutil.copytree("static", output_dir, dirs_exist_ok=True)

    nojekyll_path = os.path.join(output_dir, ".nojekyll")
    Path(nojekyll_path).touch()

    log(f"Site built successfully in {output_dir}/", use_click)
