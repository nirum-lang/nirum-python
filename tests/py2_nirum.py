import enum
import typing
import decimal
import json
import uuid

from six import text_type

from nirum.serialize import (serialize_record_type, serialize_unboxed_type,
                             serialize_meta, serialize_union_type)
from nirum.deserialize import (deserialize_record_type,
                               deserialize_unboxed_type,
                               deserialize_meta,
                               deserialize_union_type)
from nirum.validate import (validate_unboxed_type, validate_record_type,
                            validate_union_type)
from nirum.constructs import NameDict, name_dict_type
from nirum.rpc import Client, Service


class Offset(object):

    __nirum_inner_type__ = float

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return (isinstance(other, Offset) and self.value == other.value)

    def __hash__(self):
        return hash(self.value)

    def __nirum_serialize__(self):
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(cls, value):
        return deserialize_unboxed_type(cls, value)

    def __hash__(self): # noqa
        return hash((self.__class__, self.value))


class Point(object):

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

    def __init__(self, left, top):
        self.left = left
        self.top = top
        validate_record_type(self)

    def __repr__(self):
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other):
        return isinstance(other, Point) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __nirum_serialize__(self):
        return serialize_record_type(self)

    @classmethod
    def __nirum_deserialize__(cls, values):
        return deserialize_record_type(cls, values)

    def __hash__(self):
        return hash((self.__class__, self.left, self.top))


class Shape(object):

    __nirum_union_behind_name__ = 'shape'
    __nirum_field_names__ = NameDict([
    ])

    class Tag(enum.Enum):
        rectangle = 'rectangle'
        circle = 'circle'

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "{0.__module__}.{0.__qualname__} cannot be instantiated "
            "since it is an abstract class.  Instantiate a concrete subtype "
            "of it instead.".format(
                type(self)
            )
        )

    def __nirum_serialize__(self):
        pass

    @classmethod
    def __nirum_deserialize__(cls, value):
        pass


class Rectangle(Shape):

    __slots__ = (
        'upper_left',
        'lower_right'
    )
    __nirum_tag__ = Shape.Tag.rectangle
    __nirum_tag_types__ = {
        'upper_left': Point,
        'lower_right': Point
    }
    __nirum_tag_names__ = NameDict([])

    def __init__(self, upper_left, lower_right):
        self.upper_left = upper_left
        self.lower_right = lower_right
        validate_union_type(self)

    def __repr__(self):
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other):
        return isinstance(other, Rectangle) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )


class Circle(Shape):

    __slots__ = (
        'origin',
        'radius'
    )
    __nirum_tag__ = Shape.Tag.circle
    __nirum_tag_types__ = {
        'origin': Point,
        'radius': Offset
    }
    __nirum_tag_names__ = NameDict([])

    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius
        validate_union_type(self)

    def __repr__(self):
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other):
        return isinstance(other, Circle) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )


class Location(object):
    # TODO: docstring

    __slots__ = (
        'name',
        'lat',
        'lng',
    )
    __nirum_record_behind_name__ = 'location'
    __nirum_field_types__ = {
        'name': typing.Optional[text_type],
        'lat': decimal.Decimal,
        'lng': decimal.Decimal
    }
    __nirum_field_names__ = name_dict_type([
        ('name', 'name'),
        ('lat', 'lat'),
        ('lng', 'lng')
    ])

    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng
        validate_record_type(self)

    def __repr__(self):
        return '{0.__module__}.{0.__qualname__}({1})'.format(
            type(self),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other):
        return isinstance(other, Location) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __nirum_serialize__(self):
        return serialize_record_type(self)

    @classmethod
    def __nirum_deserialize__(cls, value):
        return deserialize_record_type(cls, value)


class A(object):

    __nirum_inner_type__ = text_type

    def __init__(self, value):
        validate_unboxed_type(value, text_type)
        self.value = value  # type: Text

    def __eq__(self, other):
        return (isinstance(other, A) and
                self.value == other.value)

    def __hash__(self):
        return hash(self.value)

    def __nirum_serialize__(self):
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(cls, value):
        return deserialize_unboxed_type(cls, value)

    def __repr__(self):
        return '{0.__module__}.{0.__qualname__}({1!r})'.format(
            type(self), self.value
        )


class B(object):

    __nirum_inner_type__ = A

    def __init__(self, value):
        validate_unboxed_type(value, A)
        self.value = value  # type: A

    def __eq__(self, other):
        return (isinstance(other, B) and
                self.value == other.value)

    def __hash__(self):
        return hash(self.value)

    def __nirum_serialize__(self):
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(cls, value):
        return deserialize_unboxed_type(cls, value)

    def __repr__(self):
        return '{0.__module__}.{0.__qualname__}({1!r})'.format(
            type(self), self.value
        )


class C(object):

    __nirum_inner_type__ = B

    def __init__(self, value):
        validate_unboxed_type(value, B)
        self.value = value  # type: B

    def __eq__(self, other):
        return (isinstance(other, C) and
                self.value == other.value)

    def __hash__(self):
        return hash(self.value)

    def __nirum_serialize__(self):
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(cls, value):
        return deserialize_unboxed_type(cls, value)

    def __repr__(self):
        return '{0.__module__}.{0.__qualname__}({1!r})'.format(
            type(self), self.value
        )


class HelloError(Exception):
    # compiled code

    __nirum_union_behind_name__ = 'hello_error'
    __nirum_field_names__ = name_dict_type([
        ('unknown', 'unknown'),
        ('bad_request', 'bad_request')
    ])

    class Tag(enum.Enum):
        unknown = 'unknown'
        bad_request = 'bad_request'

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "{0} cannot be instantiated "
            "since it is an abstract class.  Instantiate a concrete subtype "
            "of it instead.".format(
                (type(self).__module__ + '.' + type(self).__name__)
            )
        )

    def __nirum_serialize__(self):
        return serialize_union_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls, value
    ):
        return deserialize_union_type(cls, value)


class Unknown(HelloError):
    # compiled code

    __slots__ = ()
    __nirum_tag__ = HelloError.Tag.unknown
    __nirum_tag_types__ = {}
    __nirum_tag_names__ = name_dict_type([])

    def __init__(self, ):
        validate_union_type(self)

    def __repr__(self):
        return '{0}({1})'.format(
            (type(self).__module__ + '.' + type(self).__name__),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other):
        return isinstance(other, Unknown) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.__nirum_tag__)


class BadRequest(HelloError):
    # compiled code

    __slots__ = ()
    __nirum_tag__ = HelloError.Tag.bad_request
    __nirum_tag_types__ = {}
    __nirum_tag_names__ = name_dict_type([])

    def __init__(self, ):
        validate_union_type(self)

    def __repr__(self):
        return '{0}({1})'.format(
            (type(self).__module__ + '.' + type(self).__name__),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other):
        return isinstance(other, BadRequest) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.__nirum_tag__)


class MusicService(Service):

    __nirum_service_methods__ = {
        'get_music_by_artist_name': {
            'artist_name': text_type,
            '_return': typing.Sequence[text_type],
            '_names': NameDict([
                ('artist_name', 'artist_name')
            ])
        },
        'incorrect_return': {
            '_return': text_type,
            '_names': NameDict([])
        },
        'get_artist_by_music': {
            'music': text_type,
            '_return': text_type,
            '_names': NameDict([('music', 'norae')])
        },
        'raise_application_error_request': {
            '_return': text_type,
            '_names': NameDict([])
        },
    }
    __nirum_method_names__ = NameDict([
        ('get_music_by_artist_name', 'get_music_by_artist_name'),
        ('incorrect_return', 'incorrect_return'),
        ('get_artist_by_music', 'find_artist'),
        ('raise_application_error_request', 'raise_application_error_request'),
    ])
    __nirum_method_error_types__ = {
        'get_music_by_artist_name': HelloError
    }

    def get_music_by_artist_name(self, artist_name):
        raise NotImplementedError('get_music_by_artist_name')

    def incorrect_return(self):
        raise NotImplementedError('incorrect_return')

    def get_artist_by_music(self, music):
        raise NotImplementedError('get_artist_by_music')

    def raise_application_error_request(self):
        raise NotImplementedError('raise_application_error_request')


class MusicServiceClient(Client, MusicService):

    def get_music_by_artist_name(self, artist_name):
        meta = self.__nirum_service_methods__['get_music_by_artist_name']
        payload = {meta['_names']['artist_name']: serialize_meta(artist_name)}
        return deserialize_meta(
            meta['_return'],
            json.loads(
                self.remote_call(
                    self.__nirum_method_names__['get_music_by_artist_name'],
                    payload=payload
                )
            )
        )

    def get_artist_by_music(self, music):
        meta = self.__nirum_service_methods__['get_artist_by_music']
        payload = {meta['_names']['music']: serialize_meta(music)}
        return deserialize_meta(
            meta['_return'],
            json.loads(
                self.remote_call(
                    self.__nirum_method_names__['get_artist_by_music'],
                    payload=payload
                )
            )
        )


class Token:

    __nirum_inner_type__ = uuid.UUID

    def __init__(self, value):
        validate_unboxed_type(value, uuid.UUID)
        self.value = value

    def __eq__(self, other):
        return (isinstance(other, Token) and self.value == other.value)

    def __hash__(self):
        return hash(self.value)

    def __nirum_serialize__(self):
        return serialize_unboxed_type(self)

    @classmethod
    def __nirum_deserialize__(cls, value):
        return deserialize_unboxed_type(cls, value)


class ComplexKeyMap(object):

    __slots__ = (
        'value',
    )
    __nirum_record_behind_name__ = (
        'complex_key_map'
    )
    __nirum_field_types__ = {
        'value': typing.Mapping[Point, Point]
    }
    __nirum_field_names__ = name_dict_type([
        ('value', 'value')
    ])

    def __init__(self, value):
        self.value = value
        validate_record_type(self)

    def __repr__(self):
        return '{0}({1})'.format(
            (type(self).__module__ + '.' + type(self).__name__),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other):
        return isinstance(other, ComplexKeyMap) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other):
        return not self == other

    def __nirum_serialize__(self):
        return serialize_record_type(self)

    @classmethod
    def __nirum_deserialize__(cls, value):
        return deserialize_record_type(cls, value)

    def __hash__(self):
        return hash((self.value,))
