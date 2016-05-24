import typing

from pytest import fixture

from nirum.serialize import serialize_record_type, serialize_boxed_type
from nirum.deserialize import deserialize_record_type, deserialize_boxed_type
from nirum.validate import validate_record_type
from nirum.constructs import NameDict


class Offset:

    def __init__(self, value: float) -> None:
        self.value = value

    def __eq__(self, other) -> bool:
        return (isinstance(other, Offset) and self.value == other.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_boxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type, value: typing.Mapping[str, typing.Any]
    ) -> 'Offset':
        return deserialize_boxed_type(cls, value)


class Point:

    __slots__ = (
        'left',
        'top'
    )
    __nirum_record_behind_name__ = 'point'
    __nirum_field_types__ = {
        'left': Offset,
        'top': Offset
    }
    __nirum_field_names__ = NameDict([
        ('left', 'x')
    ])

    def __init__(self, left: Offset, top: Offset) -> None:
        self.left = left
        self.top = top
        validate_record_type(self)

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Point) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_record_type(self)

    @classmethod
    def __nirum_deserialize__(cls: type, values) -> 'Point':
        return deserialize_record_type(cls, values)


class Shape:

    __nirum_union_behind_name__ = 'shape'

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "{0.__qualname__} shouldn't be initialized because it is "
            "super-type of union. instead, use its subtype.".format(
                type(self)
            )
        )

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        pass

    @classmethod
    def __nirum_deserialize__(cls: type, value) -> 'Shape':
        pass


class Rectangle(Shape):

    __slots__ = (
        'upper_left',
        'lower_right'
    )
    __nirum_tag_behind_name__ = 'rectangle'
    __nirum_tag_types__ = {
        'upper_left': Point,
        'lower_right': Point
    }
    __nirum_tag_names__ = NameDict([])

    def __init__(self, upper_left: Point, lower_right: Point) -> None:
        self.upper_left = upper_left
        self.lower_right = lower_right

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Rectangle) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )


class Circle(Shape):

    __slots__ = (
        'origin',
        'radius'
    )
    __nirum_tag_behind_name__ = 'circle'
    __nirum_tag_types__ = {
        'origin': Point,
        'radius': Offset
    }
    __nirum_tag_names__ = NameDict([])

    def __init__(self, origin: Point, radius: Offset) -> None:
        self.origin = origin
        self.radius = radius

    def __repr__(self) -> str:
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Circle) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )


@fixture
def fx_boxed_type():
    return Offset


@fixture
def fx_offset(fx_boxed_type):
    return fx_boxed_type(1.2)


@fixture
def fx_record_type():
    return Point


@fixture
def fx_point(fx_record_type, fx_boxed_type):
    return fx_record_type(fx_boxed_type(3.14), fx_boxed_type(1.592))


@fixture
def fx_circle_type():
    return Circle


@fixture
def fx_rectangle_type():
    return Rectangle
