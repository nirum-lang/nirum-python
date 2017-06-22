# -*- coding: utf-8 -*-


import decimal,enum,json,typing,uuid



from nirum.constructs import name_dict_type
from nirum.deserialize import deserialize_boxed_type, deserialize_meta, deserialize_record_type, deserialize_union_type
from nirum.rpc import client_type, service_type
from nirum.serialize import serialize_boxed_type, serialize_meta, serialize_record_type, serialize_union_type
from nirum.validate import validate_boxed_type, validate_record_type, validate_union_type


class Offset(object):


    @staticmethod
    def __nirum_get_inner_type__():
        return float

    def __init__(self, value: float) -> None:
        validate_boxed_type(value, float)
        self.value = value  # type: float

    def __eq__(self, other) -> bool:
        return (isinstance(other, Offset) and
                self.value == other.value)

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> typing.Any:
        return serialize_boxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type,
        value: typing.Any
    ) -> 'Offset':
        return deserialize_boxed_type(cls, value)

    def __repr__(self) -> str:
        return '{0}({1!r})'.format(
            typing._type_repr(type(self)), self.value
        )

    def __hash__(self) -> int:
        return hash(self.value)



class Point(object):
    r'''
    .. attribute:: left


    .. attribute:: top


    '''
    __slots__ = (
        'left',
        'top',
    )
    __nirum_record_behind_name__ = (
        'point'
    )
    __nirum_field_names__ = name_dict_type([('left', 'x'),
        ('top', 'top')])

    @staticmethod
    def __nirum_field_types__():
        return {'left': Offset,
        'top': Offset}

    def __init__(self, left: Offset, top: Offset) -> None:
        self.left = left
        self.top = top
        validate_record_type(self)

    def __repr__(self) -> bool:
        return '{0}({1})'.format(
            typing._type_repr(type(self)),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Point) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other) -> bool:
        return not self == other

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_record_type(self)

    @classmethod
    def __nirum_deserialize__(cls: type, value) -> 'Point':
        return deserialize_record_type(cls, value)

    def __hash__(self) -> int:
        return hash((self.left, self.top,))



class Shape(object):
    r'''Type constructors in a sum type become translated to subtypes in OO
    languages, and datatypes in functional languages\.

    '''

    __nirum_union_behind_name__ = 'shape'
    __nirum_field_names__ = name_dict_type([('rectangle', 'rectangle'),
        ('circle', 'circle')])

    class Tag(enum.Enum):
        rectangle = 'rectangle'
        circle = 'circle'

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "{0} cannot be instantiated "
            "since it is an abstract class.  Instantiate a concrete subtype "
            "of it instead.".format(typing._type_repr(type(self)))
        )

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_union_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type, value
    ) -> 'Shape':
        return deserialize_union_type(cls, value)



class Rectangle(Shape):
    r'''
    .. attribute:: upper_left


    .. attribute:: lower_right


    '''
    __slots__ = (
        'upper_left',
        'lower_right'
    )
    __nirum_tag__ = Shape.Tag.rectangle
    __nirum_tag_names__ = name_dict_type([
        ('upper_left', 'upper_left'),
        ('lower_right', 'lower_right')
    ])

    @staticmethod
    def __nirum_tag_types__():
        return [('upper_left', Point),
        ('lower_right', Point)]

    def __init__(self, upper_left: Point, lower_right: Point) -> None:
        self.upper_left = upper_left
        self.lower_right = lower_right
        validate_union_type(self)

    def __repr__(self) -> str:
        return '{0}({1})'.format(
            typing._type_repr(type(self)),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Rectangle) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((self.upper_left, self.lower_right,))



class Circle(Shape):
    r'''
    .. attribute:: origin


    .. attribute:: radius


    '''
    __slots__ = (
        'origin',
        'radius'
    )
    __nirum_tag__ = Shape.Tag.circle
    __nirum_tag_names__ = name_dict_type([
        ('origin', 'origin'),
        ('radius', 'radius')
    ])

    @staticmethod
    def __nirum_tag_types__():
        return [('origin', Point),
        ('radius', Offset)]

    def __init__(self, origin: Point, radius: Offset) -> None:
        self.origin = origin
        self.radius = radius
        validate_union_type(self)

    def __repr__(self) -> str:
        return '{0}({1})'.format(
            typing._type_repr(type(self)),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Circle) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((self.origin, self.radius,))

            


class Location(object):
    r'''
    .. attribute:: name


    .. attribute:: lat


    .. attribute:: lng


    '''
    __slots__ = (
        'name',
        'lat',
        'lng',
    )
    __nirum_record_behind_name__ = (
        'location'
    )
    __nirum_field_names__ = name_dict_type([('name', 'name'),
        ('lat', 'lat'),
        ('lng', 'lng')])

    @staticmethod
    def __nirum_field_types__():
        return {'name': typing.Optional[str],
        'lat': decimal.Decimal,
        'lng': decimal.Decimal}

    def __init__(self, name: typing.Optional[str], lat: decimal.Decimal, lng: decimal.Decimal) -> None:
        self.name = name
        self.lat = lat
        self.lng = lng
        validate_record_type(self)

    def __repr__(self) -> bool:
        return '{0}({1})'.format(
            typing._type_repr(type(self)),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Location) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other) -> bool:
        return not self == other

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_record_type(self)

    @classmethod
    def __nirum_deserialize__(cls: type, value) -> 'Location':
        return deserialize_record_type(cls, value)

    def __hash__(self) -> int:
        return hash((self.name, self.lat, self.lng,))



class A(object):


    @staticmethod
    def __nirum_get_inner_type__():
        return str

    def __init__(self, value: str) -> None:
        validate_boxed_type(value, str)
        self.value = value  # type: str

    def __eq__(self, other) -> bool:
        return (isinstance(other, A) and
                self.value == other.value)

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> typing.Any:
        return serialize_boxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type,
        value: typing.Any
    ) -> 'A':
        return deserialize_boxed_type(cls, value)

    def __repr__(self) -> str:
        return '{0}({1!r})'.format(
            typing._type_repr(type(self)), self.value
        )

    def __hash__(self) -> int:
        return hash(self.value)



class B(object):


    @staticmethod
    def __nirum_get_inner_type__():
        return A

    def __init__(self, value: A) -> None:
        validate_boxed_type(value, A)
        self.value = value  # type: A

    def __eq__(self, other) -> bool:
        return (isinstance(other, B) and
                self.value == other.value)

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> typing.Any:
        return serialize_boxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type,
        value: typing.Any
    ) -> 'B':
        return deserialize_boxed_type(cls, value)

    def __repr__(self) -> str:
        return '{0}({1!r})'.format(
            typing._type_repr(type(self)), self.value
        )

    def __hash__(self) -> int:
        return hash(self.value)



class C(object):


    @staticmethod
    def __nirum_get_inner_type__():
        return B

    def __init__(self, value: B) -> None:
        validate_boxed_type(value, B)
        self.value = value  # type: B

    def __eq__(self, other) -> bool:
        return (isinstance(other, C) and
                self.value == other.value)

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> typing.Any:
        return serialize_boxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type,
        value: typing.Any
    ) -> 'C':
        return deserialize_boxed_type(cls, value)

    def __repr__(self) -> str:
        return '{0}({1!r})'.format(
            typing._type_repr(type(self)), self.value
        )

    def __hash__(self) -> int:
        return hash(self.value)



class HelloError(Exception):



    __nirum_union_behind_name__ = 'hello_error'
    __nirum_field_names__ = name_dict_type([('unknown', 'unknown'),
        ('bad_request', 'bad_request')])

    class Tag(enum.Enum):
        unknown = 'unknown'
        bad_request = 'bad_request'

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "{0} cannot be instantiated "
            "since it is an abstract class.  Instantiate a concrete subtype "
            "of it instead.".format(typing._type_repr(type(self)))
        )

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_union_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type, value
    ) -> 'HelloError':
        return deserialize_union_type(cls, value)



class Unknown(HelloError):


    __slots__ = (
        
    )
    __nirum_tag__ = HelloError.Tag.unknown
    __nirum_tag_names__ = name_dict_type([
        
    ])

    @staticmethod
    def __nirum_tag_types__():
        return []

    def __init__(self, ) -> None:
        
        validate_union_type(self)

    def __repr__(self) -> str:
        return '{0}({1})'.format(
            typing._type_repr(type(self)),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Unknown) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.__nirum_tag__)



class BadRequest(HelloError):


    __slots__ = (
        
    )
    __nirum_tag__ = HelloError.Tag.bad_request
    __nirum_tag_names__ = name_dict_type([
        
    ])

    @staticmethod
    def __nirum_tag_types__():
        return []

    def __init__(self, ) -> None:
        
        validate_union_type(self)

    def __repr__(self) -> str:
        return '{0}({1})'.format(
            typing._type_repr(type(self)),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, BadRequest) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.__nirum_tag__)

            


class MusicService(service_type):


    __nirum_schema_version__ = '0.6.0'
    __nirum_service_methods__ = {
        'get_music_by_artist_name': {
            '_v': 2,
            '_return': lambda: typing.Sequence[str],
            '_names': name_dict_type([('artist_name', 'artist_name')]),
            'artist_name': lambda: str
        },
'incorrect_return': {
            '_v': 2,
            '_return': lambda: str,
            '_names': name_dict_type([]),
            
        },
'get_artist_by_music': {
            '_v': 2,
            '_return': lambda: str,
            '_names': name_dict_type([('music', 'norae')]),
            'music': lambda: str
        },
'raise_application_error_request': {
            '_v': 2,
            '_return': lambda: str,
            '_names': name_dict_type([]),
            
        }
    }
    __nirum_method_names__ = name_dict_type([
        ('get_music_by_artist_name', 'get_music_by_artist_name'),
        ('incorrect_return', 'incorrect_return'),
        ('get_artist_by_music', 'find_artist'),
        ('raise_application_error_request', 'raise_application_error_request')
    ])

    @staticmethod
    def __nirum_method_error_types__(k, d=None):
        return dict([
            ('get_music_by_artist_name', HelloError)
        ]).get(k, d)

    
    def get_music_by_artist_name(self, artist_name: str) -> typing.Sequence[str]:
        r'''
        :param artist_name

        '''
        raise NotImplementedError('MusicService has to implement get_music_by_artist_name()')



    def incorrect_return(self, ) -> str:


        raise NotImplementedError('MusicService has to implement incorrect_return()')



    def get_artist_by_music(self, music: str) -> str:
        r'''
        :param music

        '''
        raise NotImplementedError('MusicService has to implement get_artist_by_music()')



    def raise_application_error_request(self, ) -> str:


        raise NotImplementedError('MusicService has to implement raise_application_error_request()')



# FIXME client MUST be generated & saved on diffrent module
#       where service isn't included.
class MusicService_Client(client_type, MusicService):
    
    def get_music_by_artist_name(self, artist_name: str) -> typing.Sequence[str]:
        meta = self.__nirum_service_methods__['get_music_by_artist_name']
        rtype = meta['_return']() if meta.get('_v', 1) >= 2 else meta['_return']
        return deserialize_meta(
            rtype,
            json.loads(
                self.remote_call(
                    self.__nirum_method_names__['get_music_by_artist_name'],
                    payload={meta['_names']['artist_name']: serialize_meta(artist_name)}
                )
            )
        )



    def incorrect_return(self, ) -> str:
        meta = self.__nirum_service_methods__['incorrect_return']
        rtype = meta['_return']() if meta.get('_v', 1) >= 2 else meta['_return']
        return deserialize_meta(
            rtype,
            json.loads(
                self.remote_call(
                    self.__nirum_method_names__['incorrect_return'],
                    payload={}
                )
            )
        )



    def get_artist_by_music(self, music: str) -> str:
        meta = self.__nirum_service_methods__['get_artist_by_music']
        rtype = meta['_return']() if meta.get('_v', 1) >= 2 else meta['_return']
        return deserialize_meta(
            rtype,
            json.loads(
                self.remote_call(
                    self.__nirum_method_names__['get_artist_by_music'],
                    payload={meta['_names']['music']: serialize_meta(music)}
                )
            )
        )



    def raise_application_error_request(self, ) -> str:
        meta = self.__nirum_service_methods__['raise_application_error_request']
        rtype = meta['_return']() if meta.get('_v', 1) >= 2 else meta['_return']
        return deserialize_meta(
            rtype,
            json.loads(
                self.remote_call(
                    self.__nirum_method_names__['raise_application_error_request'],
                    payload={}
                )
            )
        )

    pass



class Token(object):


    @staticmethod
    def __nirum_get_inner_type__():
        return uuid.UUID

    def __init__(self, value: uuid.UUID) -> None:
        validate_boxed_type(value, uuid.UUID)
        self.value = value  # type: uuid.UUID

    def __eq__(self, other) -> bool:
        return (isinstance(other, Token) and
                self.value == other.value)

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)

    def __nirum_serialize__(self) -> typing.Any:
        return serialize_boxed_type(self)

    @classmethod
    def __nirum_deserialize__(
        cls: type,
        value: typing.Any
    ) -> 'Token':
        return deserialize_boxed_type(cls, value)

    def __repr__(self) -> str:
        return '{0}({1!r})'.format(
            typing._type_repr(type(self)), self.value
        )

    def __hash__(self) -> int:
        return hash(self.value)



class ComplexKeyMap(object):
    r'''
    .. attribute:: value


    '''
    __slots__ = (
        'value',
    )
    __nirum_record_behind_name__ = (
        'complex_key_map'
    )
    __nirum_field_names__ = name_dict_type([('value', 'value')])

    @staticmethod
    def __nirum_field_types__():
        return {'value': typing.Mapping[Point, Point]}

    def __init__(self, value: typing.Mapping[Point, Point]) -> None:
        self.value = value
        validate_record_type(self)

    def __repr__(self) -> bool:
        return '{0}({1})'.format(
            typing._type_repr(type(self)),
            ', '.join('{}={}'.format(attr, getattr(self, attr))
                      for attr in self.__slots__)
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, ComplexKeyMap) and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.__slots__
        )

    def __ne__(self, other) -> bool:
        return not self == other

    def __nirum_serialize__(self) -> typing.Mapping[str, typing.Any]:
        return serialize_record_type(self)

    @classmethod
    def __nirum_deserialize__(cls: type, value) -> 'ComplexKeyMap':
        return deserialize_record_type(cls, value)

    def __hash__(self) -> int:
        return hash((self.value,))

