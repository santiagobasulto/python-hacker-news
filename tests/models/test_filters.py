import pytest
from calendar import timegm
from datetime import datetime

from hn import models
from hn.models import (
    PostType, Author, StoryID, And, Or, FilterParser, CreatedAtFilter,
    PointsFilter, NumCommentsFilter)


# Filters:
def test_filter_equality():
    assert CreatedAtFilter(
        datetime(2018, 1, 1), models.EQUALS_OPERATOR
    ) == CreatedAtFilter(
        datetime(2018, 1, 1), models.EQUALS_OPERATOR)

    assert CreatedAtFilter(
        datetime(2018, 1, 1), models.LESS_OPERATOR
    ) == CreatedAtFilter(
        datetime(2018, 1, 1), models.LESS_OPERATOR)

    assert CreatedAtFilter(
        datetime(2018, 1, 1), models.EQUALS_OPERATOR
    ) != CreatedAtFilter(
        datetime(2018, 1, 1), models.LESS_OPERATOR)

    assert PointsFilter(10, models.EQUALS_OPERATOR) == PointsFilter(
        10, models.EQUALS_OPERATOR)

    assert PointsFilter(10, models.LESS_OPERATOR) == PointsFilter(
        10, models.LESS_OPERATOR)

    assert PointsFilter(10, models.EQUALS_OPERATOR) != PointsFilter(
        10, models.LESS_OPERATOR)

    assert NumCommentsFilter(10, models.EQUALS_OPERATOR) == NumCommentsFilter(
        10, models.EQUALS_OPERATOR)

    assert NumCommentsFilter(10, models.LESS_OPERATOR) == NumCommentsFilter(
        10, models.LESS_OPERATOR)

    assert NumCommentsFilter(10, models.EQUALS_OPERATOR) != NumCommentsFilter(
        10, models.LESS_OPERATOR)


def test_equals_filter_mutually_exclusive():
    filter = CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR)
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_EQUALS_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_EQUALS_OPERATOR)
    ) is True


def test_less_filter_mutually_exclusive():
    filter = CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR)
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_EQUALS_OPERATOR)
    ) is True

    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR)
    ) is False
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_EQUALS_OPERATOR)
    ) is False


def test_less_equals_filter_mutually_exclusive():
    filter = CreatedAtFilter(datetime(2018, 1, 1), models.LESS_EQUALS_OPERATOR)

    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_EQUALS_OPERATOR)
    ) is True

    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR)
    ) is False
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_EQUALS_OPERATOR)
    ) is False

def test_greater_filter_mutually_exclusive():
    filter = CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR)
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_EQUALS_OPERATOR)
    ) is True

    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR)
    ) is False
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_EQUALS_OPERATOR)
    ) is False


def test_greater_equals_filter_mutually_exclusive():
    filter = CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR)
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR)
    ) is True
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_EQUALS_OPERATOR)
    ) is True

    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR)
    ) is False
    assert filter.mutually_exclusive(
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_EQUALS_OPERATOR)
    ) is False


def test_filters_hashable():
    filter_set = set([
        NumCommentsFilter(10, models.EQUALS_OPERATOR),
        NumCommentsFilter(10, models.LESS_OPERATOR),
        NumCommentsFilter(10, models.EQUALS_OPERATOR),

        CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR),
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR),
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR),

        PointsFilter(5, models.LESS_EQUALS_OPERATOR),
        PointsFilter(50, models.LESS_EQUALS_OPERATOR),
        PointsFilter(5, models.EQUALS_OPERATOR),
    ])

    assert len(filter_set) == 7
    assert filter_set == set([
        NumCommentsFilter(10, models.EQUALS_OPERATOR),
        NumCommentsFilter(10, models.LESS_OPERATOR),

        CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR),
        CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR),

        PointsFilter(5, models.LESS_EQUALS_OPERATOR),
        PointsFilter(50, models.LESS_EQUALS_OPERATOR),
        PointsFilter(5, models.EQUALS_OPERATOR),
    ])

def test_create_at_filter_parsing():
    assert CreatedAtFilter.parse(
        'created_at', '2018-01-01'
    ) == CreatedAtFilter(
        datetime(2018, 1, 1), models.EQUALS_OPERATOR
    )
    assert CreatedAtFilter.parse(
        'created_at', '2018-11-03T14:53:42.000Z'
    ) == CreatedAtFilter(
        datetime(2018, 11, 3, 14, 53, 42), models.EQUALS_OPERATOR
    )

    assert CreatedAtFilter.parse(
        'created_at', '2018'
    ) == CreatedAtFilter(
        datetime(2018, 1, 1), models.EQUALS_OPERATOR
    )

    assert CreatedAtFilter.parse(
        'created_at', datetime(2018, 1, 1)
    ) == CreatedAtFilter(
        datetime(2018, 1, 1), models.EQUALS_OPERATOR
    )

    assert CreatedAtFilter.parse(
        'created_at__lt', datetime(2018, 1, 1)
    ) == CreatedAtFilter(
        datetime(2018, 1, 1), models.LESS_OPERATOR
    )

    assert CreatedAtFilter.parse(
        'created_at__lte', datetime(2018, 1, 1)
    ) == CreatedAtFilter(
        datetime(2018, 1, 1), models.LESS_EQUALS_OPERATOR
    )

    assert CreatedAtFilter.parse(
        'created_at__gt', datetime(2018, 1, 1)
    ) == CreatedAtFilter(
        datetime(2018, 1, 1), models.GREATER_OPERATOR
    )
    assert CreatedAtFilter.parse(
        'created_at__gte', datetime(2018, 1, 1)
    ) == CreatedAtFilter(
        datetime(2018, 1, 1), models.GREATER_EQUALS_OPERATOR
    )


def test_points_filter_parsing():
    assert PointsFilter.parse('points', '10') == PointsFilter(
        10, models.EQUALS_OPERATOR)
    assert PointsFilter.parse('points__lt', '10') == PointsFilter(
        10, models.LESS_OPERATOR)
    assert PointsFilter.parse('points__lte', '10') == PointsFilter(
        10, models.LESS_EQUALS_OPERATOR)
    assert PointsFilter.parse('points__gt', '10') == PointsFilter(
        10, models.GREATER_OPERATOR)
    assert PointsFilter.parse('points__gte', '10') == PointsFilter(
        10, models.GREATER_EQUALS_OPERATOR)


def test_num_comments_filter_parsing():
    assert NumCommentsFilter.parse('num_comments', '10') == NumCommentsFilter(
        10, models.EQUALS_OPERATOR)
    assert NumCommentsFilter.parse('num_comments__lt', '10') == NumCommentsFilter(
        10, models.LESS_OPERATOR)
    assert NumCommentsFilter.parse('num_comments__lte', '10') == NumCommentsFilter(
        10, models.LESS_EQUALS_OPERATOR)
    assert NumCommentsFilter.parse('num_comments__gt', '10') == NumCommentsFilter(
        10, models.GREATER_OPERATOR)
    assert NumCommentsFilter.parse('num_comments__gte', '10') == NumCommentsFilter(
        10, models.GREATER_EQUALS_OPERATOR)


def test_created_at_filter_str():
    filter = CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR)
    assert str(filter) == 'created_at_i=1514764800'

    filter = CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR)
    assert str(filter) == 'created_at_i<1514764800'

    filter = CreatedAtFilter(datetime(2018, 1, 1), models.LESS_EQUALS_OPERATOR)
    assert str(filter) == 'created_at_i<=1514764800'

    filter = CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_OPERATOR)
    assert str(filter) == 'created_at_i>1514764800'

    filter = CreatedAtFilter(datetime(2018, 1, 1), models.GREATER_EQUALS_OPERATOR)
    assert str(filter) == 'created_at_i>=1514764800'


def test_points_filter_str():
    filter = PointsFilter(15, models.EQUALS_OPERATOR)
    assert str(filter) == 'points=15'

    filter = PointsFilter(15, models.LESS_OPERATOR)
    assert str(filter) == 'points<15'

    filter = PointsFilter(15, models.LESS_EQUALS_OPERATOR)
    assert str(filter) == 'points<=15'

    filter = PointsFilter(15, models.GREATER_OPERATOR)
    assert str(filter) == 'points>15'

    filter = PointsFilter(15, models.GREATER_EQUALS_OPERATOR)
    assert str(filter) == 'points>=15'


def test_num_comments_str():
    filter = NumCommentsFilter(7, models.EQUALS_OPERATOR)
    assert str(filter) == 'num_comments=7'

    filter = NumCommentsFilter(7, models.LESS_OPERATOR)
    assert str(filter) == 'num_comments<7'

    filter = NumCommentsFilter(7, models.LESS_EQUALS_OPERATOR)
    assert str(filter) == 'num_comments<=7'

    filter = NumCommentsFilter(7, models.GREATER_OPERATOR)
    assert str(filter) == 'num_comments>7'

    filter = NumCommentsFilter(7, models.GREATER_EQUALS_OPERATOR)
    assert str(filter) == 'num_comments>=7'


def test_filter_parser_duplicated_filters():
    FilterParser([
        CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR),
        PointsFilter(10, models.EQUALS_OPERATOR),
        PointsFilter(10, models.LESS_OPERATOR)
    ])
    with pytest.raises(ValueError):
        FilterParser([
            CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR),
            PointsFilter(10, models.EQUALS_OPERATOR),
            PointsFilter(10, models.LESS_OPERATOR),
            PointsFilter(10, models.EQUALS_OPERATOR),
        ])


def test_parse_filters():
    filters = FilterParser.parse(
        created_at='2018', points='5', num_comments__gt='10')

    assert filters._filters == [
        CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR),
        PointsFilter(5, models.EQUALS_OPERATOR),
        NumCommentsFilter(10, models.GREATER_OPERATOR)
    ]

    filters = FilterParser.parse(
        created_at__lt='2017-09', points__gte='15', num_comments__lt='100')

    assert filters._filters == [
        CreatedAtFilter(datetime(2017, 9, 1), models.LESS_OPERATOR),
        PointsFilter(15, models.GREATER_EQUALS_OPERATOR),
        NumCommentsFilter(100, models.LESS_OPERATOR)
    ]

    filters = FilterParser.parse(
        created_at__lte='2018-09', created_at__gt='2017-09',
        points__gte='15', points__lt=100,
        num_comments__lt='100', num_comments__gte='35')

    assert filters._filters == [
        CreatedAtFilter(datetime(2018, 9, 1), models.LESS_EQUALS_OPERATOR),
        CreatedAtFilter(datetime(2017, 9, 1), models.GREATER_OPERATOR),
        PointsFilter(15, models.GREATER_EQUALS_OPERATOR),
        PointsFilter(100, models.LESS_OPERATOR),
        NumCommentsFilter(100, models.LESS_OPERATOR),
        NumCommentsFilter(35, models.GREATER_EQUALS_OPERATOR),
    ]


def test_parse_filters_replace_with_replacement():
    filters = FilterParser([
        CreatedAtFilter(datetime(2017, 1, 1), models.GREATER_EQUALS_OPERATOR),
        CreatedAtFilter(datetime(2018, 11, 25), models.LESS_OPERATOR),
        PointsFilter(10, models.EQUALS_OPERATOR),
        NumCommentsFilter(5, models.GREATER_EQUALS_OPERATOR)
    ])

    new_filters = filters.replace(created_at__lt='2018-11-01')
    assert set(new_filters._filters) == set([
        CreatedAtFilter(datetime(2017, 1, 1), models.GREATER_EQUALS_OPERATOR),
        CreatedAtFilter(datetime(2018, 11, 1), models.LESS_OPERATOR),
        PointsFilter(10, models.EQUALS_OPERATOR),
        NumCommentsFilter(5, models.GREATER_EQUALS_OPERATOR)
    ])


def test_parse_filters_replace_with_new_one():
    filters = FilterParser([
        CreatedAtFilter(datetime(2017, 1, 1), models.GREATER_EQUALS_OPERATOR),
        PointsFilter(10, models.EQUALS_OPERATOR),
        NumCommentsFilter(5, models.GREATER_EQUALS_OPERATOR)
    ])

    new_filters = filters.replace(created_at__lt='2018-11-01')
    assert set(new_filters._filters) == set([
        CreatedAtFilter(datetime(2017, 1, 1), models.GREATER_EQUALS_OPERATOR),
        CreatedAtFilter(datetime(2018, 11, 1), models.LESS_OPERATOR),
        PointsFilter(10, models.EQUALS_OPERATOR),
        NumCommentsFilter(5, models.GREATER_EQUALS_OPERATOR)
    ])


def test_parse_filter_string():
    filters = FilterParser.parse(created_at='2018')
    assert str(filters) == 'created_at_i=1514764800'

    filters = FilterParser.parse(
        created_at='2018', points='5', num_comments__gt='10')
    assert str(filters) == 'created_at_i=1514764800,points=5,num_comments>10'

    filters = FilterParser.parse(
        created_at__lte='2018', points__lt='5', num_comments__gte='10')
    assert str(filters) == 'created_at_i<=1514764800,points<5,num_comments>=10'
