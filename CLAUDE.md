# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based personal academic website for Anuroop Sriram, an AI researcher at Meta FAIR. The site showcases research publications, datasets, and professional information.

## Development Commands

### Python Version (Recommended)
- `pip install -r requirements.txt` - Install Python dependencies
- `python dev.py` - Start local development server at http://localhost:5000
- `python build.py` - Build static site to `_site/` directory

### Legacy Jekyll Version
- `bundle install` - Install Ruby gem dependencies
- `jekyll serve` or `bundle exec jekyll serve` - Start local development server
- `jekyll serve --drafts` - Include draft posts in development
- `jekyll build` or `bundle exec jekyll build` - Build the static site

Note: The site has been converted to Python/Flask for easier development and deployment.

## Architecture

### Site Structure
- **`_config.yml`** - Main Jekyll configuration
- **`_data/`** - Structured data files (publications, datasets, news)
  - `publist.yml` - Publications list with metadata
  - `datalist.yml` - Datasets information  
  - `news.yml` - News/announcements
- **`_layouts/`** - HTML templates for different page types
- **`_pages/`** - Markdown content pages
- **`_includes/`** - Reusable HTML components
- **`_sass/`** - Sass/SCSS stylesheets
- **`images/`** - Static images organized by type (pubpic/, teampic/, etc.)

### Key Features
- Publication management via YAML data files
- Responsive Bootstrap-based design
- Google Analytics integration
- Academic paper image thumbnails and links

### Content Management
- Publications are managed in `_data/publist.yml` with fields for title, authors, venue, year, etc.
- Each publication can have associated images in `images/pubpic/`
- News items are in `_data/news.yml`
- Main content pages are in `_pages/` as Markdown files

### Theme and Styling
- Uses Bootstrap 3 with custom Sass overrides
- Custom layouts for different content types (publications, home, etc.)
- Responsive design with sidebar navigation

This is a static Jekyll site focused on academic content presentation with structured data management for publications and research outputs.