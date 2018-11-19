# HackerNews / Algolia Python Library

This is a simple library to interface with [HN Search API](https://hn.algolia.com/api) (provided by Algolia).

### Install instructions

```bash
$ pip install python-hn
```

### Usage

##### Search by date

```python
from hn import search_by_date, PostType

# Search everything (stories, comments, etc)
search_by_date(q='lisp', author='pg', created_at__lt='2018-01-01')

# Search only stories
search_by_date(q='lisp', author='pg', tags=PostType('story'), created_at__lt='2018-01-01')

# Search stories *or* comments (see tags below)
search_by_date(
    q='lisp', author='pg',
    tags=(PostType('story') | PostType('comment')),
    created_at__lt='2018-01-01')
```

Parameters received by `search_by_date`:
* `q` (optional): The query string to search for
* `author` (optional): Author's username
* `tags`: Tags to apply (see [section _Tags_ below](#tags))
* `hits_per_page` (optional, default=1000): Number of posts to return per request.
* `**filters`: Other filters to apply (date, points, number of comments). See [section _Filters_ below](#filters).

##### Tags

Tags are part of HN Search API provided by Algolia. You can read more in [their docs](https://hn.algolia.com/api). They can form complex queries, for example:

```python
# Stories by `pg` or comments by `patio11`
tags = (PostType('story') & Author('pg')) | (PostType('comment') & Author('patio11'))

# All the comments in the story `6902129`
tags = PostType('comment') & StoryID('6902129')
```

The available tags are:
* `PostType`: with options `story`, `comment`, `poll`, `pollopt`, `show_hn`, `ask_hn`, `front_page`.
* `Author`: receives the username as param (`Author('pg')`).
* `StoryID`: receives the story id (`StoryID('6902129')`)


##### Filters

Filters can be applied to restrict the search by:

* Creation Date: `created_at`
* Points: `points`
* Number of comments: `num_comments`

They can accept `>, <, >=, <=` operators with a syntax similar to Django's.
* `lt` (`<`): Lower than. Example `ponts__lt=100`
* `lte` (`<=`): Lower than or equals to. Example `ponts__lte=100`
* `gt` (`>`): Greater than. Example `created_at__gt='2018'` (created after 2018-01-01).
* `gte` (`>=`): Greater than or equals to. Example `num_comments__gte=50`.

Examples (See [Algolia docs](https://hn.algolia.com/api) for more info):

```python
# Created after October 1st, 2018
search_by_date(created_at__gt='2018-10')

# Created after October 1st, 2017 and before January 1st 2018
search_by_date(created_at__gt='2018-10', created_at__lt='2018')

# Stories with *exactly* 1000 points
search_by_date(tags=PostType('story'), points=1000)

# Comments with more than 50 points
search_by_date(tags=PostType('comment'), points__gt=50)

# Stories with 100 comments or more
search_by_date(tags=PostType('story'), num_comments__gt=100)
```

##### Search

_[TODO]_
