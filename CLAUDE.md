# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python/Flask personal academic website for Anuroop Sriram, an AI researcher at Meta FAIR. The site showcases research publications, datasets, and professional information. It uses Frozen-Flask to generate a static site deployed to GitHub Pages.

## Development Commands

- `pip install -r requirements.txt` - Install Python dependencies
- `python dev.py` - Start local development server at http://localhost:5001
- `python build.py` - Build static site to `docs/` directory

With uv:
- `uv sync` - Install dependencies
- `uv run website-dev` - Start development server
- `uv run website-build` - Build static site

## Architecture

### Site Structure
- **`src/website/`** - Main Python package
  - `app.py` - Flask application factory
  - `config.py` - Site configuration (title, description, analytics)
  - `data_loader.py` - Loads YAML data files
  - `filters.py` - Jinja2 template filters
  - `routes.py` - URL route definitions
  - `builder.py` - Shared build logic (SASS compilation, static file copying, site freezing)
  - `cli.py` - Click-based CLI entry points
- **`templates/`** - Jinja2 templates
  - `layouts/` - Base layouts (base.html, homelay.html, gridlay.html)
  - `includes/` - Reusable components (head, header, footer, sidebar, pub_card)
  - `pages/` - Page templates (home, publications, datasets, code, etc.)
- **`static/`** - Static assets (CSS/SCSS, JS, images, fonts)
- **`_data/`** - YAML data files driving site content
  - `publist.yml` - Publications list with metadata
  - `datalist.yml` - Datasets information
  - `codelist.yml` - Code/project repositories
  - `pi.yml` - Principal investigator profile and education
  - `years.yml` - Year list for publication grouping
  - `news.yml` - News/announcements
- **`docs/`** - Built static site output (served by GitHub Pages)

### Key Features
- Publication management via YAML data files, grouped by year
- Responsive Bootstrap 3 design with light/dark theme toggle
- Google Analytics integration
- Academic paper image thumbnails and links
- SCSS compiled via libsass

### Content Management
- Publications are managed in `_data/publist.yml` with fields for title, authors, venue, year, arxiv, code, data, etc.
- Publication images go in `static/images/pubpic/`
- Dataset images go in `static/images/datapic/`
- Site configuration lives in `src/website/config.py`

### Build Process
`python build.py` (or `uv run website-build`) runs the shared build logic in `src/website/builder.py`:
1. Compiles SCSS from `static/css/main.scss` to CSS
2. Copies external assets (images, fonts, JS) into `static/`
3. Freezes all Flask routes into static HTML in `docs/`
4. Copies static assets into `docs/` for deployment
