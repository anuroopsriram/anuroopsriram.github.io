"""Jinja2 template filters for the website."""

import json
import re
from typing import Any, Dict, List, Optional

from markupsafe import Markup


CREATOR_PERSON = {
    "@type": "Person",
    "@id": "https://www.wikidata.org/entity/Q138516652",
    "name": "Anuroop Sriram",
}


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
    return Markup(str(text).replace(name, f'<strong>{name}</strong>'))


def _clean_text(text: Optional[str]) -> str:
    """Strip HTML tags and collapse whitespace for JSON-LD text fields."""
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', '', str(text))
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _parse_authors(raw: Optional[str]) -> List[Dict[str, str]]:
    """Split a comma-separated author string into Schema.org Person objects."""
    if not raw:
        return []
    authors: List[Dict[str, str]] = []
    for name in str(raw).split(','):
        name = name.strip()
        if not name:
            continue
        authors.append({"@type": "Person", "name": name})
    return authors


def publication_jsonld_filter(publi: Dict[str, Any], site_url: str = 'https://anuroopsriram.com') -> Markup:
    """Build a Schema.org ScholarlyArticle JSON-LD blob for a publication."""
    if not publi:
        return Markup('')

    article: Dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": _clean_text(publi.get('title')),
        "name": _clean_text(publi.get('title')),
        "author": _parse_authors(publi.get('authors')),
        "creator": CREATOR_PERSON,
    }

    if publi.get('year') is not None:
        article["datePublished"] = str(publi['year'])

    venue = publi.get('venue')
    if venue:
        article["isPartOf"] = {"@type": "Periodical", "name": _clean_text(venue)}

    publisher = publi.get('publisher') or publi.get('organization')
    if publisher:
        article["publisher"] = {"@type": "Organization", "name": _clean_text(publisher)}

    abstract = _clean_text(publi.get('abstract'))
    if abstract:
        article["abstract"] = abstract

    keywords = publi.get('keywords') or []
    if keywords:
        article["keywords"] = ', '.join(str(k) for k in keywords)

    same_as: List[str] = []
    if publi.get('arxiv'):
        same_as.append(f"https://arxiv.org/abs/{publi['arxiv']}")
    if publi.get('doi'):
        same_as.append(f"https://doi.org/{publi['doi']}")
    if publi.get('journal'):
        same_as.append(publi['journal'])
    elif publi.get('link'):
        same_as.append(publi['link'])
    if publi.get('patent'):
        same_as.append(publi['patent'])
    if same_as:
        article["sameAs"] = same_as

    if publi.get('image'):
        article["image"] = f"{site_url}/static/images/pubpic/{publi['image']}"

    if publi.get('code'):
        article["codeRepository"] = publi['code']

    return Markup(json.dumps(article, ensure_ascii=False))


def dataset_jsonld_filter(dataset: Dict[str, Any], site_url: str = 'https://anuroopsriram.com') -> Markup:
    """Build a Schema.org Dataset JSON-LD blob for a dataset entry."""
    if not dataset:
        return Markup('')

    obj: Dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": _clean_text(dataset.get('title')),
        "description": _clean_text(dataset.get('description')),
        "creator": CREATOR_PERSON,
    }

    if dataset.get('category'):
        obj["keywords"] = dataset['category']

    if dataset.get('project_url'):
        obj["url"] = dataset['project_url']

    if dataset.get('data_url'):
        obj["distribution"] = [{
            "@type": "DataDownload",
            "contentUrl": dataset['data_url'],
        }]

    if dataset.get('code_url'):
        obj["codeRepository"] = dataset['code_url']

    if dataset.get('image'):
        obj["image"] = f"{site_url}/static/images/datapic/{dataset['image']}"

    return Markup(json.dumps(obj, ensure_ascii=False))


def itemlist_jsonld_filter(
    items: List[Dict[str, Any]],
    page_url: str,
    page_name: str,
    name_key: str = 'title',
) -> Markup:
    """Build a Schema.org CollectionPage wrapping an ItemList of named items."""
    if items is None:
        items = []

    item_list_elements = []
    for idx, item in enumerate(items, start=1):
        element: Dict[str, Any] = {
            "@type": "ListItem",
            "position": idx,
            "name": _clean_text(item.get(name_key) or ''),
        }
        item_list_elements.append(element)

    obj = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": page_name,
        "url": page_url,
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(items),
            "itemListElement": item_list_elements,
        },
    }
    return Markup(json.dumps(obj, ensure_ascii=False))


def register_filters(app):
    """Register all template filters with the Flask app."""
    app.template_filter('newline_to_br')(newline_to_br_filter)
    app.template_filter('strip_html')(strip_html_filter)
    app.template_filter('strip_newlines')(strip_newlines_filter)
    app.template_filter('truncate')(truncate_filter)
    app.template_filter('truncate_authors')(truncate_authors_filter)
    app.template_filter('bold_name')(bold_name_filter)
    app.template_filter('publication_jsonld')(publication_jsonld_filter)
    app.template_filter('dataset_jsonld')(dataset_jsonld_filter)
    app.template_filter('itemlist_jsonld')(itemlist_jsonld_filter)