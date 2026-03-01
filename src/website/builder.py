"""Shared build logic for the website."""

import os
import shutil
from typing import Optional

import sass
from flask import Flask
from flask_frozen import Freezer

from .app import create_app

DEFAULT_OUTPUT_DIR = 'docs'


def log(message: str, use_click: bool = False) -> None:
    if use_click:
        import click
        click.echo(message)
    else:
        print(message)


def compile_sass(use_click: bool = False) -> None:
    """Compile SASS files to CSS."""
    log("Compiling SASS...", use_click)
    os.makedirs('static/css', exist_ok=True)
    css_content = sass.compile(filename='static/css/main.scss')
    with open('static/css/main.css', 'w') as f:
        f.write(css_content)
    log("SASS compilation complete.", use_click)


def copy_static_files(use_click: bool = False) -> None:
    """Copy static files to the static directory."""
    log("Copying static files...", use_click)

    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/fonts', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

    for src_dir, dst_dir in [('images', 'static/images'),
                              ('fonts', 'static/fonts'),
                              ('js', 'static/js')]:
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

    if os.path.exists('CNAME'):
        shutil.copy2('CNAME', 'static/')

    log("Static files copied.", use_click)


def build_site(output_dir: Optional[str] = None, use_click: bool = False) -> None:
    """Build the static site."""
    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', '..', DEFAULT_OUTPUT_DIR
        )
        output_dir = os.path.normpath(output_dir)

    log("Building static site...", use_click)

    app = create_app('production')
    app.config['FREEZER_DESTINATION'] = output_dir
    app.config['FREEZER_RELATIVE_URLS'] = True
    app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True
    freezer = Freezer(app)

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    compile_sass(use_click)
    copy_static_files(use_click)
    freezer.freeze()

    if os.path.exists('static'):
        for item in os.listdir('static'):
            src = os.path.join('static', item)
            dst = os.path.join(output_dir, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)

    log(f"Site built successfully in {output_dir}/", use_click)
