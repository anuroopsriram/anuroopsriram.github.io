#!/usr/bin/env python3
"""Build script for generating static site from Flask app."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from website.builder import build_site

if __name__ == '__main__':
    build_site()
