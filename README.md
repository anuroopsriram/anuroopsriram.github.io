# Anuroop Sriram - Academic Website

A modern Python Flask-based academic website showcasing research publications, datasets, and professional information.

## 🚀 Quick Start

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Start development server
uv run website-dev

# Build for production
uv run website-build
```

### Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
python dev.py

# Build for production
python build.py
```

## 🏗️ Project Structure

```
├── src/website/           # Main application package
│   ├── __init__.py       # Package initialization
│   ├── app.py            # Flask application factory
│   ├── builder.py        # Shared build logic
│   ├── config.py         # Configuration settings
│   ├── data_loader.py    # YAML data loading utilities
│   ├── filters.py        # Jinja2 template filters
│   ├── routes.py         # URL route definitions
│   └── cli.py            # Command line interface
├── templates/             # Jinja2 templates
│   ├── layouts/          # Base page layouts
│   ├── includes/         # Reusable components
│   └── pages/            # Page-specific templates
├── static/               # Static assets
│   ├── css/              # Stylesheets (SCSS)
│   ├── js/               # JavaScript files
│   ├── images/           # Images and media
│   └── fonts/            # Web fonts
├── _data/                # YAML data files
│   ├── publist.yml       # Publications
│   ├── datalist.yml      # Datasets
│   ├── news.yml          # News items
│   └── ...               # Other data files
├── docs/                 # Generated static site (build output, served by GitHub Pages)
├── pyproject.toml        # Project configuration and dependencies
└── requirements.txt      # pip-compatible dependencies
```

## 🛠️ Development

### Code Quality Tools

The project uses modern Python tooling:

- **ruff**: Fast linting and formatting
- **mypy**: Static type checking
- **pre-commit**: Git hooks for code quality

```bash
# Install development dependencies
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Run linting
ruff check src/

# Run formatting
ruff format src/

# Run type checking
mypy src/
```

### Commands

| Command | Description |
|---------|-------------|
| `uv run website-dev` | Start development server |
| `uv run website-build` | Build static site |
| `python dev.py` | Alternative dev server |
| `python build.py` | Alternative build script |

## 📝 Content Management

### Publications
Edit `_data/publist.yml` to manage publications. Each entry supports:
- Title, authors, venue, year
- Links to paper, code, datasets
- Associated images

### Datasets
Manage datasets in `_data/datalist.yml` with similar structure.

### News
Add news items to `_data/news.yml` for the homepage sidebar.

## 🎨 Theming

The website supports light and dark themes with:
- CSS custom properties for theme variables
- Automatic theme persistence
- Toggle button in navigation
- Smooth transitions between themes

## 🚀 Deployment

### GitHub Pages
```bash
# Build the site
uv run website-build

# The docs/ directory contains the static site
# GitHub Pages is configured to serve from docs/ on the master branch
```

### Other Platforms
The generated `docs/` directory is a complete static website that works with:
- Netlify
- Vercel
- AWS S3
- Any web server

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'production' for production builds
- `SECRET_KEY`: Flask secret key (for any session-based features)

### Site Configuration
Edit `src/website/config.py` to update:
- Site title and description
- Contact information
- Google Analytics ID
- Other site-wide settings

## 📦 Dependencies

### Core Dependencies
- **Flask**: Web framework
- **Frozen-Flask**: Static site generation
- **PyYAML**: YAML data processing
- **libsass**: SCSS compilation
- **Jinja2**: Template engine

### Development Dependencies
- **ruff**: Linting and formatting
- **mypy**: Type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙋‍♂️ Support

For issues or questions:
- Open an issue on GitHub
- Contact: anuroop.sriram@gmail.com