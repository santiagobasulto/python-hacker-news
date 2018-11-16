# HackerNews / Algolia Python Library

> **This is a work in progress**

This is a simple library to interface with [HN Search API](https://hn.algolia.com/api) (provided by Algolia).

### Install instructions

```bash
$ pip install python-hn
```

### Usage

##### Search by date

```python
from hn import search_by_date

search_by_date(q='apple', author='pg', created_at__lt='2018-01-01')
```


##### Search

_[TODO]_
