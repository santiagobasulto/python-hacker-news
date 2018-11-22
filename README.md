# HackerNews / Algolia Python Library

This is a simple library to interface with [HN Search API](https://hn.algolia.com/api) (provided by Algolia).

[Install](#install-instructions) | [Basic Usage](#usage) | [Development](#development) | [Roadmap](#roadmap)

## Install instructions

```bash
$ pip install python-hn
```

## Usage

**Check out [Interactive Docs](https://notebooks.rmotr.com/santiagobasulto/python-hn-library-interactive-docs-d49b8026) to try the library without installing it.**

```python
from hn import search_by_date

# Search everything (stories, comments, etc) containing the keyword 'python'
search_by_date('python')


# Search everything (stories, comments, etc) from author 'pg' and keyword 'lisp'
search_by_date('lisp', author='pg', created_at__lt='2018-01-01')

# Search only stories
search_by_date('lisp', author='pg', stories=True, created_at__lt='2018-01-01')

# Search stories *or* comments
search_by_date(q='lisp', author='pg', stories=True, comments=True, created_at__lt='2018-01-01')
```

##### Tags

Tags are part of HN Search API provided by Algolia. You can read more in [their docs](https://hn.algolia.com/api). They can form complex queries, for example:

```python
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

## Development

Current milestone: https://github.com/santiagobasulto/python-hacker-news/milestone/2

## Roadmap

* V0.0.4: Other endpoints: /search, /users, /items (**CURRENT**)
* V0.0.3: Post type aliases, improved API
* V0.0.2: Functioning API
* V0.0.1: Initial Version
