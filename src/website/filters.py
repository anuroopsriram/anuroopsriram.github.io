"""Jinja2 template filters for the website."""

import re
from typing import Optional


def escape_filter(text: Optional[str]) -> str:
    """Escape text for HTML."""
    if text is None:
        return ''
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def newline_to_br_filter(text: Optional[str]) -> str:
    """Convert newlines to HTML breaks."""
    if text is None:
        return ''
    return str(text).replace('\n', '<br/>')


def strip_html_filter(text: Optional[str]) -> str:
    """Basic HTML tag removal."""
    if text is None:
        return ''
    return re.sub(r'<[^>]+>', '', str(text))


def strip_newlines_filter(text: Optional[str]) -> str:
    """Remove newlines."""
    if text is None:
        return ''
    return str(text).replace('\n', ' ').replace('\r', ' ')


def truncate_filter(text: Optional[str], length: int = 160) -> str:
    """Truncate text to specified length."""
    if text is None:
        return ''
    text = str(text)
    return text[:length] + '...' if len(text) > length else text


def truncate_authors_filter(text: Optional[str], max_authors: int = 3) -> str:
    """Show first N authors and append 'et al.' if there are more."""
    if text is None:
        return ''
    authors = [a.strip() for a in str(text).split(',')]
    if len(authors) <= max_authors:
        return text
    return ', '.join(authors[:max_authors]) + ', et al.'


def bold_name_filter(text: Optional[str], name: str = 'Anuroop Sriram') -> str:
    """Bold a specific name in an author list."""
    if text is None:
        return ''
    from markupsafe import Markup
    return Markup(str(text).replace(name, f'<strong>{name}</strong>'))


def register_filters(app):
    """Register all template filters with the Flask app."""
    app.template_filter('escape')(escape_filter)
    app.template_filter('newline_to_br')(newline_to_br_filter)
    app.template_filter('strip_html')(strip_html_filter)
    app.template_filter('strip_newlines')(strip_newlines_filter)
    app.template_filter('truncate')(truncate_filter)
    app.template_filter('truncate_authors')(truncate_authors_filter)
    app.template_filter('bold_name')(bold_name_filter)