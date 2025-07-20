"""Route definitions for the website."""

from flask import Blueprint, render_template

# Create blueprint for main routes
main = Blueprint('main', __name__)


@main.route('/')
def home():
    """Home page route."""
    return render_template('pages/home.html', 
                         page={'title': None, 'permalink': '/'})


@main.route('/publications/')
def publications():
    """Publications page route."""
    return render_template('pages/publications.html',
                         page={'title': 'Publications', 'permalink': '/publications/'})


@main.route('/datasets/')
def datasets():
    """Datasets page route."""
    return render_template('pages/datasets.html',
                         page={'title': 'Datasets', 'permalink': '/datasets/'})


@main.route('/code/')
def code():
    """Code page route."""
    return render_template('pages/code.html',
                         page={'title': 'Code', 'permalink': '/code/'})


@main.route('/allnews/')
def allnews():
    """All news page route."""
    return render_template('pages/allnews.html',
                         page={'title': 'News', 'permalink': '/allnews/'})


@main.route('/aboutwebsite/')
def aboutwebsite():
    """About website page route."""
    return render_template('pages/aboutwebsite.html',
                         page={'title': 'About this website', 'permalink': '/aboutwebsite/'})