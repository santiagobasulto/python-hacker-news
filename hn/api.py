import requests

from . import endpoints

def search(q=None, author=None, story_id=None, stories=None, comments=None,
           show_hn=None, ask_hn=None, front_page=None, polls=None,
           pollopt=None, created_before=None, ):
           pass

def search_hn_by_date(q=None, tags=None, before_date=None, hits_per_page=1000):
    params = {
        'hitsPerPage': hits_per_page
    }
    if tags:
        params['tags'] = str(tags)
    if before_date:
        assert type(before_date) == datetime
        params['numericFilters'] = 'created_at_i<{}'.format(int(before_date.timestamp()))

    while True:
        resp = requests.get(endpoints.SEARCH_BY_DATE, params=params)
        resp.raise_for_status()
        doc = resp.json()
        if not doc['hits']:
            return
        for hit in doc['hits']:
            yield hit
        params['numericFilters'] = 'created_at_i<{}'.format(hit['created_at_i'])


search("rmotr", "pg", stories=True, comments=True, **filters)
search("rmotr", "pg", stories=True, comments=True, created_at__lt=2018)

# F(created__lt=dt) & F(created__gt=dt) & F(points=50)
