import pytest
from calendar import timegm
from datetime import datetime

from hn import models
from hn.models import (
    PostType, Author, StoryID, And, Or, FilterParser, CreatedAtFilter,
    PointsFilter, NumCommentsFilter)


def test_equality_of_boolean_operators():
    assert And(PostType('story'), PostType('comment')) == And(PostType('story'), PostType('comment'))
    assert And(PostType('story'), Author('pg')) == And(PostType('story'), Author('pg'))

    assert Or(PostType('story'), PostType('comment')) == Or(PostType('story'), PostType('comment'))
    assert Or(PostType('story'), Author('pg')) == Or(PostType('story'), Author('pg'))

    assert And(PostType('story'), PostType('pg')) != And(PostType('story'), Author('pg'))
    assert Or(PostType('story'), PostType('pg')) != Or(PostType('story'), Author('pg'))

    assert And(PostType('story'), PostType('show_hn')) != And(PostType('story'), PostType('comment'))
    assert Or(PostType('story'), PostType('show_hn')) != Or(PostType('story'), PostType('comment'))


def test_equality_of_tags():
    assert PostType('story') == PostType('story')
    assert Author('pg') == Author('pg')
    assert PostType('story') != PostType('comment')


def test_operators_on_tags():
    assert (PostType('story') & Author('pg')) == And(PostType('story'), Author('pg'))
    assert (PostType('story') | PostType('comment')) == Or(PostType('story'), PostType('comment'))


def test_operators_combined():
    assert And(PostType('story'), Author('pg')) & StoryID(281) == And(
        And(PostType('story'), Author('pg')),
        StoryID(281)
    )
    assert Or(PostType('story'), PostType('comment')) & Author('pg')== And(
        Or(PostType('story'), PostType('comment')),
        Author('pg')
    )


def test_stringify_tags():
    assert str(PostType('story')) == 'story'
    assert str(Author('pg')) == 'author_pg'
    assert str(StoryID(1832)) == 'story_1832'


def test_stringify_simple_and():
    assert str(And(PostType('story'), Author('pg'))) == 'story,author_pg'
    assert str(And(PostType('comment'), StoryId(819))) == 'comment,story_819'

def test_stringify_simple_and():
    assert str(Or(PostType('story'), PostType('comment'))) == '(story,comment)'
    assert str(Or(PostType('comment'), Author('pg'))) == '(comment,author_pg)'
    assert str(Or(StoryID('182'), StoryID('983'))) == '(story_182,story_983)'


def test_stringify_complex_booleans():
    comp1 = And(Author('pg'), Or(PostType('story'), PostType('poll')))
    comp2 = Or(
        And(
            PostType('comment'), Author('pg')
        ),
        And(
            PostType('poll'), Author('dhouston')
        )
    )
    comp1 = And(Author('pg'), Or(PostType('story'), PostType('poll')))

    assert str(comp1) == 'author_pg,(story,poll)'
    # assert str(comp2) == '()'


def test_stingify_operated_tags():
    cond1 = PostType('story') & Author('pg')
    assert str(cond1) == 'story,author_pg'

    cond2 = (PostType('story') | PostType('comment')) & Author('pg')
    assert str(cond2) == '(story,comment),author_pg'


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
    with pytest.raises(ValueError):
        FilterParser([
            CreatedAtFilter(datetime(2018, 1, 1), models.LESS_OPERATOR),
            PointsFilter(10, models.EQUALS_OPERATOR),
            PointsFilter(10, models.LESS_OPERATOR)
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

def test_parse_filters_replace():
    filters = FilterParser([
        CreatedAtFilter(datetime(2017, 1, 1), models.LESS_OPERATOR),
        PointsFilter(10, models.EQUALS_OPERATOR),
        NumCommentsFilter(5, models.GREATER_EQUALS_OPERATOR)
    ])

    assert set(filters.replace(created_at='2018')._filters) == set([
        CreatedAtFilter(datetime(2018, 1, 1), models.EQUALS_OPERATOR),
        PointsFilter(10, models.EQUALS_OPERATOR),
        NumCommentsFilter(5, models.GREATER_EQUALS_OPERATOR)
    ])
    assert set(filters.replace(points__gte='5')._filters) == set([
        CreatedAtFilter(datetime(2017, 1, 1), models.LESS_OPERATOR),
        PointsFilter(5, models.GREATER_EQUALS_OPERATOR),
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
