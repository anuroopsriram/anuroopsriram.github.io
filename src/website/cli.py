"""Command line interface for the website."""

import os
import sys
import shutil
import sass
from flask_frozen import Freezer
import click

from .app import create_app


@click.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--debug/--no-debug', default=True, help='Enable debug mode')
def dev(host: str, port: int, debug: bool) -> None:
    """Start development server."""
    app = create_app('development')
    app.config['ENV'] = 'development'
    
    click.echo("Starting development server...")
    click.echo(f"Open http://localhost:{port} in your browser")
    click.echo("Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")


def compile_sass() -> None:
    """Compile SASS files to CSS."""
    click.echo("Compiling SASS...")
    
    # Ensure css directory exists
    os.makedirs('static/css', exist_ok=True)
    
    # Compile main.scss
    css_content = sass.compile(
        filename='static/css/main.scss',
        include_paths=['_sass', '_sass/bootstrap']
    )
    
    with open('static/css/main.css', 'w') as f:
        f.write(css_content)
    
    click.echo("SASS compilation complete.")


def copy_static_files() -> None:
    """Copy static files to the static directory."""
    click.echo("Copying static files...")
    
    # Create static directories
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/fonts', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Copy images
    if os.path.exists('images'):
        shutil.copytree('images', 'static/images', dirs_exist_ok=True)
    
    # Copy fonts
    if os.path.exists('fonts'):
        shutil.copytree('fonts', 'static/fonts', dirs_exist_ok=True)
    
    # Copy CNAME if it exists
    if os.path.exists('CNAME'):
        shutil.copy2('CNAME', 'static/')
    
    click.echo("Static files copied.")


@click.command()
@click.option('--output-dir', default='_site', help='Output directory for built site')
def build(output_dir: str) -> None:
    """Build the static site."""
    click.echo("Building static site...")
    
    # Create Flask app
    app = create_app('production')
    
    # Configure freezer
    app.config['FREEZER_DESTINATION'] = output_dir
    app.config['FREEZER_RELATIVE_URLS'] = True
    app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True
    freezer = Freezer(app)
    
    # Clean previous build
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Compile SASS
    compile_sass()
    
    # Copy static files
    copy_static_files()
    
    # Generate static site
    freezer.freeze()
    
    # Copy static files to output directory
    if os.path.exists('static'):
        for item in os.listdir('static'):
            src = os.path.join('static', item)
            dst = os.path.join(output_dir, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    
    click.echo(f"Site built successfully in {output_dir}/")


@click.group()
def cli() -> None:
    """Academic website CLI."""
    pass


cli.add_command(dev)
cli.add_command(build)


if __name__ == '__main__':
    cli()