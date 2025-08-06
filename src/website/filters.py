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


def register_filters(app):
    """Register all template filters with the Flask app."""
    app.template_filter('escape')(escape_filter)
    app.template_filter('newline_to_br')(newline_to_br_filter)
    app.template_filter('strip_html')(strip_html_filter)
    app.template_filter('strip_newlines')(strip_newlines_filter)
    app.template_filter('truncate')(truncate_filter)