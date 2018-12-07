import json
import pytest
from pathlib import Path

import responses

from hn import search_by_date
from hn import api
from hn.models import PostType, StoryID
from hn import tags

BASE_PATH = Path(__file__).parent
REQUESTS_PATH = BASE_PATH / 'requests'

def test_shortcut_params_to_tags():
    assert api._shortcut_params_to_tags(stories=True) == tags.Story
    assert api._shortcut_params_to_tags(story_id=18823) == StoryID('18823')

    assert api._shortcut_params_to_tags(
        stories=True, comments=True) == PostType('story') | PostType('comment')
    assert api._shortcut_params_to_tags(
        stories=True, comments=True, ask_hn=True, polls=True
    ) == tags.Story | tags.Comment | tags.AskHN | tags.Poll

    assert api._shortcut_params_to_tags(
        story_id=18823, stories=True) == StoryID('18823') & tags.Story

    assert api._shortcut_params_to_tags(
        story_id=18823, stories=True, comments=True
    ) == StoryID('18823') & (tags.Story | tags.Comment)


@responses.activate
def test_search_by_date_tags_post_type_params_mutually_exclusive():
    """Tags and post type params should not be mixed up together"""
    with pytest.raises(ValueError):
        res = search_by_date('lisp', 'pg', stories=True, tags=tags.Comment)
        next(res)
    with pytest.raises(ValueError):
        res = search_by_date('lisp', stories=True, tags=tags.Comment)
        next(res)
    with pytest.raises(ValueError):
        res = search_by_date(stories=True, tags=tags.Comment)
        next(res)


@responses.activate
def test_search_by_date_with_query_default_params():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&numericFilters=created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date('rmotr', hits_per_page=2)
    post = next(res)
    assert post['story_id'] == 18445714

    post = next(res)
    assert post['story_id'] == 18462671

    post = next(res)
    assert post['story_id'] == 18460087

    post = next(res)
    assert post['story_id'] == 18457200


@responses.activate
def test_search_by_date_with_query_and_author_post_types_params():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comment),author_pg',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comment),author_pg&numericFilters=created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date(
        'rmotr', author='pg', stories=True, comments=True,
        hits_per_page=2)
    post = next(res)
    assert post['story_id'] == 18445714

    post = next(res)
    assert post['story_id'] == 18462671

    post = next(res)
    assert post['story_id'] == 18460087

    post = next(res)
    assert post['story_id'] == 18457200


@responses.activate
def test_search_by_date_with_query_and_author_multiple_post_types_params():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comment,show_hn,ask_hn,poll),author_pg',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comment,show_hn,ask_hn,poll),author_pg&numericFilters=created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date(
        'rmotr', author='pg', stories=True, comments=True, polls=True,
        ask_hn=True, show_hn=True, hits_per_page=2)
    post = next(res)
    assert post['story_id'] == 18445714

    post = next(res)
    assert post['story_id'] == 18462671

    post = next(res)
    assert post['story_id'] == 18460087

    post = next(res)
    assert post['story_id'] == 18457200


@responses.activate
def test_search_by_date_with_query_and_author_post_types():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comment),author_pg',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comment),author_pg&numericFilters=created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date(
        'rmotr', author='pg', tags=(PostType('story') | PostType('comment')),
        hits_per_page=2)
    post = next(res)
    assert post['story_id'] == 18445714

    post = next(res)
    assert post['story_id'] == 18462671

    post = next(res)
    assert post['story_id'] == 18460087

    post = next(res)
    assert post['story_id'] == 18457200


@responses.activate
def test_search_by_date_with_query_and_author_post_types_aliases():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comment),author_pg',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comment),author_pg&numericFilters=created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date(
        'rmotr', author='pg', tags=(tags.Story | tags.Comment),
        hits_per_page=2)
    post = next(res)
    assert post['story_id'] == 18445714

    post = next(res)
    assert post['story_id'] == 18462671

    post = next(res)
    assert post['story_id'] == 18460087

    post = next(res)
    assert post['story_id'] == 18457200


@responses.activate
def test_search_by_date_without_query_default_params():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date(hits_per_page=2)
    post = next(res)
    assert post['story_id'] == 18445714

    post = next(res)
    assert post['story_id'] == 18462671

    post = next(res)
    assert post['story_id'] == 18460087

    post = next(res)
    assert post['story_id'] == 18457200


@responses.activate
def test_search_by_date_without_query_default_params():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date(hits_per_page=2)
    post = next(res)
    assert post['story_id'] == 18445714

    post = next(res)
    assert post['story_id'] == 18462671

    post = next(res)
    assert post['story_id'] == 18460087

    post = next(res)
    assert post['story_id'] == 18457200


@responses.activate
def test_search_by_date_without_query_created_parameter():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i>1514764800',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i>1514764800,created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date(hits_per_page=2, created_at__gt='2018')
    post = next(res)
    assert post['story_id'] == 18445714

    post = next(res)
    assert post['story_id'] == 18462671

    post = next(res)
    assert post['story_id'] == 18460087

    post = next(res)
    assert post['story_id'] == 18457200

@responses.activate
def test_search_by_date_with_query_created_and_points():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i>1514764800,points=50',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i>1514764800,points=50,created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date(hits_per_page=2, created_at__gt='2018', points=50)
    post = next(res)
    assert post['story_id'] == 18445714

    post = next(res)
    assert post['story_id'] == 18462671

    post = next(res)
    assert post['story_id'] == 18460087

    post = next(res)
    assert post['story_id'] == 18457200


@responses.activate
def test_items_endpoint_is_found():
    with (REQUESTS_PATH / 'item.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/items/18562744',
            json=json.loads(fp.read()), status=200)

    post = api.get_item(18562744)

    assert post['id'] == 18562744
    assert post['author'] == 'santiagobasulto'
    assert len(post['children']) == 4


@responses.activate
def test_items_endpoint_not_found():
    with (REQUESTS_PATH / 'item.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/items/0000',
            status=404)

    post = api.get_item('0000')
    assert post is None
