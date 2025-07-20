#!/usr/bin/env python3
"""
Build script for generating static site from Flask app.
"""

import os
import shutil
import sass
from flask_frozen import Freezer
from app import app

# Configure freezer
app.config['FREEZER_DESTINATION'] = '_site'
app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)

def compile_sass():
    """Compile SASS files to CSS."""
    print("Compiling SASS...")
    
    # Ensure css directory exists
    os.makedirs('static/css', exist_ok=True)
    
    # Compile main.scss
    css_content = sass.compile(
        filename='static/css/main.scss',
        include_paths=['_sass', '_sass/bootstrap']
    )
    
    with open('static/css/main.css', 'w') as f:
        f.write(css_content)
    
    print("SASS compilation complete.")

def copy_static_files():
    """Copy static files to the static directory."""
    print("Copying static files...")
    
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
    
    # Copy JavaScript
    if os.path.exists('js'):
        shutil.copytree('js', 'static/js', dirs_exist_ok=True)
    
    # Copy CNAME if it exists
    if os.path.exists('CNAME'):
        shutil.copy2('CNAME', 'static/')
    
    print("Static files copied.")

def build_site():
    """Build the static site."""
    print("Building static site...")
    
    # Clean previous build
    if os.path.exists('_site'):
        shutil.rmtree('_site')
    
    # Compile SASS
    compile_sass()
    
    # Copy static files
    copy_static_files()
    
    # Configure freezer to ignore missing files
    app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True
    
    # Generate static site
    freezer.freeze()
    
    # Copy static files to _site
    if os.path.exists('static'):
        for item in os.listdir('static'):
            src = os.path.join('static', item)
            dst = os.path.join('_site', item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    
    print("Site built successfully in _site/")

if __name__ == '__main__':
    build_site()