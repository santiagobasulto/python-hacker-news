import requests

from . import endpoints
from .models import FilterParser, Author, PostType


def search(q=None, author=None, story_id=None, stories=None, comments=None,
           show_hn=None, ask_hn=None, front_page=None, polls=None,
           pollopt=None, created_before=None, ):
           raise NotImplementedError()


def search_by_date(q=None, author=None, tags=None, hits_per_page=1000,
                   **filters):
    params = {
        'hitsPerPage': hits_per_page
    }
    if q:
        params['query'] = q

    if author:
        author_tag = Author(author)
        if not tags:
            tags = author_tag
        else:
            tags = tags & author_tag
    if tags:
        params['tags'] = str(tags)

    parser = None
    if filters:
        parser = FilterParser.parse(**filters)
        params['numericFilters'] = str(parser)

    while True:
        resp = requests.get(endpoints.SEARCH_BY_DATE, params=params)
        resp.raise_for_status()
        doc = resp.json()
        if not doc['hits']:
            return
        for hit in doc['hits']:
            yield hit
        if not parser:
            parser = FilterParser.parse(created_at__lt=hit['created_at'])
        else:
            parser = parser.replace(created_at__lt=hit['created_at'])

        params['numericFilters'] = str(parser)
