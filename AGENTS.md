# AGENTS.md

This file provides guidance to coding agents (Cursor, Claude Code, etc.) when working with code in this repository.

## Project Overview

This is a Python/Flask personal academic website for Anuroop Sriram, an AI for Science researcher. The site showcases research publications, datasets, and professional information. It uses Frozen-Flask to generate a static site deployed to GitHub Pages.

## Development Commands

With uv (recommended):
- `uv sync` - Install dependencies
- `uv run website-dev` - Start local development server at http://localhost:5001
- `uv run website-build` - Build static site to `docs/` directory

With pip:
- `pip install -e .` - Install the package (provides the `website-dev` / `website-build` commands)
- `website-dev` - Start the development server
- `website-build` - Build the static site

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
  - `pages/` - Page templates (home, publications, datasets, allnews, aboutwebsite, llms_full.txt)
- **`static/`** - Static assets
  - `css/main.scss` - design tokens, layout, and shared components; imports the page-specific partials `_home.scss`, `_pages.scss`, and `_motion.scss`
  - `js/theme.js` - light/dark theme toggle; `js/hero.js` - self-contained WebGL2 home-page hero
  - `images/`, `fonts/`
- **`data/`** - YAML data files driving site content
  - `publist.yml` - Publications list with metadata
  - `datalist.yml` - Datasets information
  - `pi.yml` - Principal investigator profile and education
  - `years.yml` - Year list for publication grouping
  - `news.yml` - News/announcements
- **`docs/`** - Built static site output (served by GitHub Pages)

### Key Features
- Publication management via YAML data files, grouped by year, with keyword filters and a sticky year-jump rail
- Custom design system (no CSS framework): oklch/`light-dark()` color tokens, Fraunces/Inter/Spline Sans Mono fonts, light/dark theme toggle
- WebGL2 "crystal lattice" hero on the home page (`static/js/hero.js`) with reduced-motion and no-WebGL fallbacks
- Cross-document view transitions, speculation-rules prerendering, and CSS scroll-driven reveal animations (all progressive enhancement)
- Google Analytics integration
- Academic paper image thumbnails and links
- SCSS compiled via libsass. Gotchas: use SCSS nesting (plain CSS nesting does not compile), `@supports selector(...)` conditions are rejected, and `min(var(--x), ...)` fails because SCSS shadows CSS `min()`; unknown plain-CSS functions like `oklch()` and `light-dark()` pass through fine

### Content Management
- Publications are managed in `data/publist.yml` with fields for title, authors, venue, year, arxiv, code, data, etc.
- Publication images go in `static/images/pubpic/`
- Dataset images go in `static/images/datapic/`
- Site configuration lives in `src/website/config.py`

### Build Process
`uv run website-build` runs the shared build logic in `src/website/builder.py`:
1. Compiles SCSS from `static/css/main.scss` (and its `_*.scss` partials) to `static/css/main.css`
2. Freezes all Flask routes into static HTML in `docs/`
3. Copies the entire `static/` tree into `docs/` for deployment

## Common Agentic Tasks

All site content is data-driven via YAML files in `data/`. After any content change, rebuild with `uv run website-build` so `docs/` stays in sync (the pre-commit hook also rebuilds `docs/`).

### Add a publication

Append a new entry to `data/publist.yml` (entries are grouped by `year` on the publications page). Fields:

- `title` (required) - publication title.
- `authors` (required) - comma-separated author list. "Anuroop Sriram" is automatically bolded in the UI and linked in the JSON-LD structured data.
- `key` (required) - short unique identifier.
- `keywords` - YAML list (e.g. `[AI for Science, Datasets]`); drives the filter buttons on the publications page. Prefer reusing existing keywords.
- `year` (required) - publication year. The year must also exist in `data/years.yml` for the entry to appear under a year heading.
- `image` - filename placed in `static/images/pubpic/` (e.g. `mypaper.webp`).
- `highlight: true` - surfaces the entry under "Selected Publications" on the home page.
- Optional links/metadata: `arxiv`, `code`, `data`, `models`, `venue`, `journal`, `doi`, `link`, `patent`, `abstract`.

### Add a dataset

Append a new entry to `data/datalist.yml` (grouped by `category` on the datasets page). Fields:

- `title` (required), `category` (required; reuse an existing category to group, or add a new one).
- `description` - short summary.
- `image` (placed in `static/images/datapic/`) or `video`.
- `project_url`, `data_url`, `code_url` - render as PROJECT / DATA / CODE buttons.
- `license` - license URL.

### Add a news item

Prepend a new entry to `data/news.yml` (newest first; shown on the home page sidebar and the news page). Fields:

- `date` - free-text string (e.g. `"February 2026"`).
- `headline` - text with inline HTML allowed (e.g. `<a href='...'>...</a>`, `<b>...</b>`).

### Build and deploy

1. Make the content/code change.
2. Run `uv run website-build` to regenerate `docs/`.
3. Commit the source change and the rebuilt `docs/` together (`docs/` is the committed GitHub Pages output).
4. Push and open a PR. GitHub Pages serves `docs/` from the `master` branch.
