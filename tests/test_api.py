import json
from pathlib import Path

import responses

from hn import search_by_date
from hn.models import PostType

BASE_PATH = Path(__file__).parent
REQUESTS_PATH = BASE_PATH / 'requests'

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
def test_search_by_date_with_query_and_author_post_types():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comments),author_pg',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?query=rmotr&hitsPerPage=2&tags=(story,comments),author_pg&numericFilters=created_at_i<1542316220',
            json=json.loads(fp.read()), status=200)

    res = search_by_date(
        'rmotr', author='pg', tags=(PostType('story') | PostType('comments')),
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
def test_search_by_date_with_query_created_parameter():
    with (REQUESTS_PATH / '1.1.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i>1514764800',
            json=json.loads(fp.read()), status=200)
    with (REQUESTS_PATH / '1.2.json').open() as fp:
        responses.add(
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i<1542316220',
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
            responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i<1542316220,points=50',
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

#
# @responses.activate
# def test_2_search_by_date_with_query_default_params():
#     with (REQUESTS_PATH / '1.1.json').open() as fp:
#         responses.add(
#             responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2',
#             json=json.loads(fp.read()), status=200)
#     with (REQUESTS_PATH / '1.2.json').open() as fp:
#         responses.add(
#             responses.GET, 'https://hn.algolia.com/api/v1/search_by_date?hitsPerPage=2&numericFilters=created_at_i<1542316220',
#             json=json.loads(fp.read()), status=200)
#
#     res = search_by_date('rmotr', hits_per_page=2)
#     post = next(res)
#     assert post['story_id'] == 18445714
#
#     post = next(res)
#     assert post['story_id'] == 18462671
#
#     post = next(res)
#     assert post['story_id'] == 18460087
#
#     post = next(res)
#     assert post['story_id'] == 18457200
