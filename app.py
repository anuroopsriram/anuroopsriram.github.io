#!/usr/bin/env python3
"""Main entry point for the academic website application."""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from website.app import create_app

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'default'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)