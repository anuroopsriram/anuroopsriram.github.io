# Python Academic Website

This is a Python Flask-based conversion of the original Jekyll academic website. It maintains the same structure and styling while using Python for static site generation.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy static assets:**
   ```bash
   # Copy images, fonts, and JavaScript files to static/ directory
   cp -r images/ static/
   cp -r fonts/ static/
   cp -r js/ static/
   cp CNAME static/ # if deploying to GitHub Pages
   ```

## Development

**Start development server:**
```bash
python dev.py
```

The site will be available at http://localhost:5000

## Build for Production

**Generate static site:**
```bash
python build.py
```

The static site will be generated in the `_site/` directory.

## Structure

- `app.py` - Main Flask application with routes and configuration
- `build.py` - Build script for generating static site using Frozen-Flask
- `dev.py` - Development server script
- `templates/` - Jinja2 templates (converted from Jekyll layouts)
  - `layouts/` - Base layouts
  - `includes/` - Reusable components
  - `pages/` - Page templates
- `static/` - Static assets (CSS, JS, images, fonts)
- `_data/` - YAML data files (unchanged from Jekyll version)

## Data Management

The site uses the same YAML data files as the Jekyll version:

- `_data/publist.yml` - Publications
- `_data/datalist.yml` - Datasets
- `_data/news.yml` - News items
- `_data/years.yml` - Publication years
- `_data/pi.yml` - Personal information
- `_data/codelist.yml` - Code repositories

## Deployment

The generated `_site/` directory contains a complete static website that can be deployed to any web server or static hosting service like GitHub Pages, Netlify, or Vercel.

## Key Differences from Jekyll

1. Uses Flask + Frozen-Flask instead of Jekyll
2. Jinja2 templates instead of Liquid templates
3. Python YAML loading instead of Jekyll's built-in YAML support
4. libsass for SCSS compilation instead of Jekyll's Sass processor
5. Flask url_for() for asset URLs instead of Jekyll's asset tags