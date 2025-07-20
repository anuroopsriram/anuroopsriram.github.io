#!/usr/bin/env python3
"""
Flask application for generating the academic website.
Converts Jekyll-based site to Python/Flask with static generation.
"""

import os
import yaml
from flask import Flask, render_template, url_for
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SITE_TITLE'] = 'Anuroop Sriram'
app.config['SITE_EMAIL'] = 'anuroop.sriram@gmail.com'
app.config['SITE_DESCRIPTION'] = 'Personal webpage of Anuroop Sriram'
app.config['SITE_BASEURL'] = ''
app.config['SITE_URL'] = ''
app.config['GOOGLE_ANALYTICS'] = 'G-H1K2L7JV60'
app.config['GROUP_PUB_BY_YEAR'] = True

def load_yaml_data(filename):
    """Load YAML data from _data directory."""
    try:
        with open(f'_data/{filename}', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or []
    except FileNotFoundError:
        return []

def get_site_data():
    """Load all site data."""
    return {
        'publist': load_yaml_data('publist.yml'),
        'datalist': load_yaml_data('datalist.yml'),
        'news': load_yaml_data('news.yml'),
        'years': load_yaml_data('years.yml'),
        'codelist': load_yaml_data('codelist.yml'),
        'pi': load_yaml_data('pi.yml')
    }

# Template context processor
@app.context_processor
def inject_site_data():
    """Inject site configuration and data into all templates."""
    return {
        'site': {
            'title': app.config['SITE_TITLE'],
            'email': app.config['SITE_EMAIL'],
            'description': app.config['SITE_DESCRIPTION'],
            'baseurl': app.config['SITE_BASEURL'],
            'url': app.config['SITE_URL'],
            'google_analytics': app.config['GOOGLE_ANALYTICS'],
            'group_pub_by_year': app.config['GROUP_PUB_BY_YEAR'],
            'data': get_site_data()
        }
    }

@app.route('/')
def home():
    """Home page route."""
    return render_template('pages/home.html', 
                         page={'title': None, 'permalink': '/'})

@app.route('/publications/')
def publications():
    """Publications page route."""
    return render_template('pages/publications.html',
                         page={'title': 'Publications', 'permalink': '/publications/'})

@app.route('/datasets/')
def datasets():
    """Datasets page route."""
    return render_template('pages/datasets.html',
                         page={'title': 'Datasets', 'permalink': '/datasets/'})

@app.route('/code/')
def code():
    """Code page route."""
    return render_template('pages/code.html',
                         page={'title': 'Code', 'permalink': '/code/'})

@app.route('/allnews/')
def allnews():
    """All news page route."""
    return render_template('pages/allnews.html',
                         page={'title': 'News', 'permalink': '/allnews/'})

@app.route('/aboutwebsite/')
def aboutwebsite():
    """About website page route."""
    return render_template('pages/aboutwebsite.html',
                         page={'title': 'About this website', 'permalink': '/aboutwebsite/'})

# Template filters
@app.template_filter('escape')
def escape_filter(text):
    """Escape text for HTML."""
    if text is None:
        return ''
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

@app.template_filter('newline_to_br')
def newline_to_br_filter(text):
    """Convert newlines to HTML breaks."""
    if text is None:
        return ''
    return str(text).replace('\n', '<br/>')

@app.template_filter('strip_html')
def strip_html_filter(text):
    """Basic HTML tag removal."""
    if text is None:
        return ''
    import re
    return re.sub(r'<[^>]+>', '', str(text))

@app.template_filter('strip_newlines')
def strip_newlines_filter(text):
    """Remove newlines."""
    if text is None:
        return ''
    return str(text).replace('\n', ' ').replace('\r', ' ')

@app.template_filter('truncate')
def truncate_filter(text, length=160):
    """Truncate text to specified length."""
    if text is None:
        return ''
    text = str(text)
    return text[:length] + '...' if len(text) > length else text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)