import requests
import functools

from . import endpoints
from . import tags as tag_aliases
from .models import FilterParser, Author, PostType, StoryID


def _shortcut_params_to_tags(**params):
    params = {k: v for k, v in params.items() if v}

    PARAMS_TAG_MAP = {
        'stories': tag_aliases.Story,
        'comments': tag_aliases.Comment,
        'show_hn': tag_aliases.ShowHN,
        'ask_hn': tag_aliases.AskHN,
        'front_page': tag_aliases.FrontPage,
        'polls': tag_aliases.Poll,
        'pollopt': tag_aliases.Pollopt,
    }
    tags = None
    if 'story_id' in params:
        tags = StoryID(params['story_id'])
        del params['story_id']

    post_type_tags = None
    if len(params) == 1:
        post_type_tags = PARAMS_TAG_MAP[next(iter(params))]
    elif len(params) > 1:
        tag_list = [PARAMS_TAG_MAP[param] for param in params]
        post_type_tags = functools.reduce(lambda x, y: x | y, tag_list)

    if tags and post_type_tags:
        return tags & post_type_tags
    elif tags:
        return tags
    return post_type_tags


def search(q=None, author=None, story_id=None, stories=None, comments=None,
           show_hn=None, ask_hn=None, front_page=None, polls=None,
           pollopt=None, created_before=None, ):
           raise NotImplementedError()


def search_by_date(q=None, author=None, story_id=None, stories=None,
                   comments=None, show_hn=None, ask_hn=None, front_page=None,
                   polls=None, pollopt=None, tags=None, hits_per_page=1000,
                   **filters):
    params = {
        'hitsPerPage': hits_per_page
    }
    shortcut_params_defined = any([
        story_id, stories, comments, show_hn, ask_hn,
        front_page, polls, pollopt])

    if shortcut_params_defined and tags:
            raise ValueError("Can't combine shortcut parameters and tags")
    if q:
        params['query'] = q

    if shortcut_params_defined:
        tags = _shortcut_params_to_tags(
            story_id=story_id, stories=stories, comments=comments,
            show_hn=show_hn, ask_hn=ask_hn, front_page=front_page,
            polls=polls, pollopt=pollopt)

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
