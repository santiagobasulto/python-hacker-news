from collections import namedtuple
from calendar import timegm

from . import utils


class Comparable:
    def __eq__(self, other):
        return (self.__class__ == other.__class__) and (self._get_value() == other._get_value())

    def __ne__(self, other):
        return not (self == other)


class BooleanOperable:
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)


class BaseBooleanOperator(Comparable):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def _get_value(self):
        return (self.left, self.right)


class And(BaseBooleanOperator, BooleanOperable):
    def __str__(self):
        return "{},{}".format(self.left, self.right)

class Or(BaseBooleanOperator, BooleanOperable):
    def __str__(self):
        return "({},{})".format(self.left, self.right)


class Tag(BooleanOperable, Comparable):
    def __init__(self, value):
        self.value = value

    def _get_value(self):
        return self.value

    def __str__(self):
        if getattr(self, 'PREFIX', None):
            return '{}_{}'.format(self.PREFIX, self.value)

        return self.value


class PostType(Tag):
    pass


class Author(Tag):
    PREFIX = 'author'


class StoryID(Tag):
    PREFIX = 'story'


FilterOperator = namedtuple('FilterOperator', ['name', 'operator'])

EQUALS_OPERATOR = FilterOperator('equals', '=')
LESS_OPERATOR = FilterOperator('less_than', '<')
LESS_EQUALS_OPERATOR = FilterOperator('less_than_equals_to', '<=')
GREATER_OPERATOR = FilterOperator('greater_than', '>')
GREATER_EQUALS_OPERATOR = FilterOperator('greater_than_equals_to', '>=')

OPERATOR_ALIASES = {
    'lt': LESS_OPERATOR,
    'lte': LESS_EQUALS_OPERATOR,
    'gt': GREATER_OPERATOR,
    'gte': GREATER_EQUALS_OPERATOR,
}


class Filter(Comparable):
    FILTER_PREFIX = None

    def __init__(self, value, operator):
        self.value = value
        self.operator = operator

    def __hash__(self):
        return hash((self.__class__, self.value, self.operator))

    @classmethod
    def parse_value(cls, value):
        return value

    @classmethod
    def matches(cls, filter_name):
        return filter_name.startswith(cls.FILTER_PREFIX)

    @classmethod
    def parse(cls, filter_name, value):
        if not cls.FILTER_PREFIX:
            raise NotImplementedError()
        if not cls.matches(filter_name):
            raise ValueError("Filter name doesn't match prefix")

        operator = EQUALS_OPERATOR
        if filter_name != cls.FILTER_PREFIX:
            if '__' not in filter_name:
                raise ValueError('Invalid filter format FILTER__operator')
            name, op = filter_name.split('__')
            operator = OPERATOR_ALIASES[op]

        return cls(cls.parse_value(value), operator)

    def _get_value(self):
        return (self.value, self.operator)

    def __repr__(self):
        return '{}({}, {})'.format(
            self.__class__.__name__, repr(self.value), repr(self.operator))

    def get_value(self):
        return self.value

    def __str__(self):
        field_name = getattr(self, 'FIELD_NAME', self.FILTER_PREFIX)
        return "{field_name}{operator}{value}".format(
            field_name=field_name,
            operator=self.operator.operator,
            value=self.get_value())


class NumericFilter(Filter):
    @classmethod
    def parse_value(cls, value):
        return int(value)


class CreatedAtFilter(Filter):
    FILTER_PREFIX = 'created_at'
    FIELD_NAME = 'created_at_i'

    @classmethod
    def parse_value(cls, value):
        return utils.parse_date(value)

    def get_value(self):
        return str(timegm(self.value.timetuple()))


class PointsFilter(NumericFilter):
    FILTER_PREFIX = 'points'


class NumCommentsFilter(NumericFilter):
    FILTER_PREFIX = 'num_comments'


class FilterParser:
    REGISTERED_FILTER_CLASSES = [
        CreatedAtFilter, PointsFilter, NumCommentsFilter
    ]

    def __init__(self, filters):
        if len(filters) != len(set(filters)):
            raise ValueError('Repeated filters found')
        self._filters = filters

    def replace(self, **new_filters):
        _new_filters = self.parse(**new_filters)._filters.copy()
        _new_classes = [f.__class__ for f in _new_filters]

        for filter in self._filters:
            if filter.__class__ not in _new_classes:
                _new_filters.append(filter)

        return FilterParser(_new_filters)

    @classmethod
    def _parse_from_list(cls, filter_name, value):
        for FilterClass in cls.REGISTERED_FILTER_CLASSES:
            if FilterClass.matches(filter_name):
                return FilterClass.parse(filter_name, value)

    @classmethod
    def parse(cls, **filters):
        if len(filters) == 0:
            raise ValueError("Need filters to parse")
        _filters = []
        for filter_name, value in filters.items():
            filter = cls._parse_from_list(filter_name, value)
            if not filter:
                raise InvalidFilterException(
                    "Can't parse %s, no filters registered" % filter_name)
            _filters.append(filter)
        return cls(_filters)

    def __str__(self):
        return ','.join([str(f) for f in self._filters])
