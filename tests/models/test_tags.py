import pytest
from calendar import timegm
from datetime import datetime

from hn import models
from hn.tags import Story, Comment, AskHN, ShowHN, Poll
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
    assert StoryID('18302') == StoryID('18302')
    assert StoryID('18302') == StoryID(18302)

    assert StoryID('18302') != StoryID('18301')
    assert PostType('story') != PostType('comment')

def test_equality_of_aliases():
    assert Story == PostType('story')
    assert Comment == PostType('comment')
    assert Poll == PostType('poll')
    assert AskHN == PostType('ask_hn')
    assert ShowHN == PostType('show_hn')


def test_operators_on_tags():
    assert (PostType('story') & Author('pg')) == And(PostType('story'), Author('pg'))
    assert (PostType('story') | PostType('comment')) == Or(PostType('story'), PostType('comment'))
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

    cond3 = (PostType('story') | PostType('comment') | PostType('ask_hn'))
    assert str(cond3) == '(story,comment,ask_hn)'

    cond4 = (PostType('story') | PostType('comment') | PostType('ask_hn')) & Author('pg')
    assert str(cond4) == '(story,comment,ask_hn),author_pg'

    cond5 = Author('pg') & (PostType('story') | PostType('comment') | PostType('ask_hn'))
    assert str(cond5) == 'author_pg,(story,comment,ask_hn)'
