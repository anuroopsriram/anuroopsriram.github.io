"""Command line interface for the website."""

import click

from .app import create_app
from .builder import build_site


@click.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5001, help='Port to bind to')
@click.option('--debug/--no-debug', default=True, help='Enable debug mode')
def dev(host: str, port: int, debug: bool) -> None:
    """Start development server."""
    app = create_app('development')

    click.echo("Starting development server...")
    click.echo(f"Open http://localhost:{port} in your browser")
    click.echo("Press Ctrl+C to stop the server")

    try:
        app.run(debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")


@click.command()
@click.option('--output-dir', default=None, help='Output directory for built site')
def build(output_dir: str) -> None:
    """Build the static site."""
    build_site(output_dir=output_dir, use_click=True)


@click.group()
def cli() -> None:
    """Academic website CLI."""
    pass


cli.add_command(dev)
cli.add_command(build)


if __name__ == '__main__':
    cli()
