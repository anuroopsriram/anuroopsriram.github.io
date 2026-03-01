"""Route definitions for the website."""

from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('pages/home.html',
                         page={'title': None, 'permalink': '/'},
                         active_page='home')


@main.route('/publications/')
def publications():
    return render_template('pages/publications.html',
                         page={'title': 'Publications', 'permalink': '/publications/'},
                         active_page='publications')


@main.route('/datasets/')
def datasets():
    return render_template('pages/datasets.html',
                         page={'title': 'Datasets', 'permalink': '/datasets/'},
                         active_page='datasets')


@main.route('/code/')
def code():
    return render_template('pages/code.html',
                         page={'title': 'Code', 'permalink': '/code/'},
                         active_page='code')


@main.route('/allnews/')
def allnews():
    return render_template('pages/allnews.html',
                         page={'title': 'News', 'permalink': '/allnews/'},
                         active_page='news')


@main.route('/aboutwebsite/')
def aboutwebsite():
    return render_template('pages/aboutwebsite.html',
                         page={'title': 'About this website', 'permalink': '/aboutwebsite/'},
                         active_page='about')
