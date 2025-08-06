#!/usr/bin/env python3
"""
Build script for generating static site from Flask app.
"""

import os
import sys
import shutil
import sass
from flask_frozen import Freezer

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from website.app import create_app

# Create Flask app
app = create_app('production')

# Configure freezer with absolute path
import os
project_root = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(project_root, 'docs')
app.config['FREEZER_DESTINATION'] = output_dir
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
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Compile SASS
    compile_sass()
    
    # Copy static files
    copy_static_files()
    
    # Configure freezer to ignore missing files
    app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True
    
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
                # Ensure destination directory exists
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
    
    print(f"Site built successfully in {output_dir}/")

if __name__ == '__main__':
    build_site()