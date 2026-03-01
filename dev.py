#!/usr/bin/env python3
"""
Development server script.
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from website.app import create_app
from website.builder import compile_sass

# Compile SCSS before starting
compile_sass()

# Create Flask app
app = create_app('development')

if __name__ == '__main__':
    print("Starting development server...")
    print("Open http://localhost:5001 in your browser")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\nServer stopped.")
