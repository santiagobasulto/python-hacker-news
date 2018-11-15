from datetime import datetime

AVAILABLE_DATE_FORMATS = [
    '%Y',
    '%Y-%m',
    '%Y-%m-%d',
    '%Y-%m-%d %H:%M:%S',
    "%Y-%m-%dT%H:%M:%S.%fZ"
]

def parse_date(dt):
    if isinstance(dt, datetime):
        return dt

    for format in AVAILABLE_DATE_FORMATS:
        try:
            return datetime.strptime(dt, format)
        except ValueError:
            pass

    raise ValueError("Invalid date format, see AVAILABLE_DATE_FORMATS")
