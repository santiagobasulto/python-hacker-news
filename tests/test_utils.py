import pytest
from datetime import datetime

from hn import utils


def test_parse_date():
    assert utils.parse_date(datetime(2018, 1, 1)) == datetime(2018, 1, 1)
    assert utils.parse_date('2018-07-01') == datetime(2018, 7, 1)
    assert utils.parse_date('2018-09-03 18:45:11') == datetime(2018, 9, 3, 18, 45, 11)
    assert utils.parse_date('2018-09-03 18:45:11') == datetime(2018, 9, 3, 18, 45, 11)
    assert utils.parse_date('2018-11-03T14:53:42.000Z') == datetime(
        2018, 11, 3, 14, 53, 42)

    assert utils.parse_date('2018') == datetime(2018, 1, 1)
    assert utils.parse_date('2018-09') == datetime(2018, 9, 1)

    with pytest.raises(ValueError):
        utils.parse_date('2018-13')
