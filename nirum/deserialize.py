""":mod:`nirum.deserialize`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import datetime
import decimal
import enum
import numbers
import typing
import uuid

from iso8601 import iso8601, parse_date
from six import text_type

from .datastructures import Map
from ._compat import get_tuple_param_types, get_union_types, is_union_type

__all__ = (
    'deserialize_abstract_type',
    'deserialize_boxed_type',
    'deserialize_iterable_abstract_type',
    'deserialize_meta',
    'deserialize_optional',
    'deserialize_primitive',
    'deserialize_record_type',
    'deserialize_tuple_type',
    'deserialize_unboxed_type',
    'deserialize_union_type',
    'is_support_abstract_type',
)
_NIRUM_PRIMITIVE_TYPE = {
    float, decimal.Decimal, uuid.UUID, datetime.datetime,
    datetime.date, bool, int, text_type, numbers.Integral
}


def is_support_abstract_type(t):
    """FIXME: 3.5 only"""
    if hasattr(t, '__origin__') and t.__origin__:
        data_type = t.__origin__
    else:
        data_type = t
    abstract_types = {
        typing.Sequence,
        typing.List,
        typing.Set,
        typing.AbstractSet,
        typing.Mapping,
        typing.Dict,
    }
    return any(type_ is data_type for type_ in abstract_types)


def deserialize_iterable_abstract_type(cls, cls_origin_type, data):
    abstract_type_map = {
        typing.Sequence: list,
        typing.List: list,
        typing.Set: set,
        typing.AbstractSet: set,
        typing.Mapping: Map,
    }
    deserialized_data = data
    cls_primitive_type = abstract_type_map[cls_origin_type]
    # Whereas on Python/typing < 3.5.2 type parameters are stored in
    # __parameters__ attribute, on Python/typing >= 3.5.2 __parameters__
    # attribute is gone and __args__ comes instead.
    type_params = (cls.__args__
                   if hasattr(cls, '__args__')
                   else cls.__parameters__)
    if len(type_params) == 1:
        elem_type, = type_params
        if isinstance(elem_type, typing.TypeVar):
            deserialized_data = cls_primitive_type(data)
        else:
            deserialized_data = cls_primitive_type(
                deserialize_meta(elem_type, d) for d in data
            )
    elif len(type_params) == 2:
        # Key-value
        key_type, value_type = type_params
        assert not (isinstance(key_type, typing.TypeVar) or
                    isinstance(value_type, typing.TypeVar))
        if not isinstance(data, collections.Sequence):
            raise ValueError('map must be an array of item objects e.g. '
                             '[{"key": ..., "value": ...}, ...]')

        def parse_pair(pair):
            if not isinstance(pair, collections.Mapping):
                raise ValueError('map item must be a JSON object')
            try:
                key = pair['key']
                value = pair['value']
            except KeyError:
                raise ValueError('map item must consist of "key" and "value" '
                                 'fields e.g. {"key": ..., "value": ...}')
            return (
                deserialize_meta(key_type, key),
                deserialize_meta(value_type, value),
            )
        deserialized_data = cls_primitive_type(map(parse_pair, data))
    return deserialized_data


def deserialize_abstract_type(cls, data):
    abstract_type_map = {
        typing.Sequence: list,
        typing.List: list,
        typing.Dict: dict,
        typing.Set: set,
        typing.AbstractSet: set,
    }
    cls_origin_type = cls.__origin__
    if cls_origin_type is None:
        cls_origin_type = cls
    iterable_types = {
        typing.Sequence, typing.List, typing.Tuple, typing.Set,
        typing.AbstractSet, typing.Mapping,
    }
    if cls_origin_type in iterable_types:
        return deserialize_iterable_abstract_type(cls, cls_origin_type, data)
    else:
        return abstract_type_map[cls_origin_type](data)


def deserialize_tuple_type(cls, data):
    tuple_types = get_tuple_param_types(cls)
    if tuple_types is None and isinstance(data, tuple):
        return data
    tuple_type_length = len(tuple_types)
    data_length = len(data)
    if not tuple_types:
        return tuple(data)
    if tuple_type_length != data_length:
        raise ValueError(
            'Expected {}-tuple, not {}-tuple'.format(
                tuple_type_length, data_length
            )
        )
    return tuple(
        deserialize_meta(t, d)
        for t, d in zip(tuple_types, data)
    )


def deserialize_primitive(cls, data):
    if cls is datetime.datetime:
        try:
            d = parse_date(data)
        except iso8601.ParseError:
            raise ValueError("'{}' is not a datetime.".format(data))
    elif cls is datetime.date:
        try:
            d = parse_date(data).date()
        except iso8601.ParseError:
            raise ValueError("'{}' is not a date.".format(data))
    elif cls in {int, float, uuid.UUID, bool}:
        d = cls(data)
    elif cls is numbers.Integral:
        d = data
    elif cls is decimal.Decimal:
        try:
            d = cls(data)
        except decimal.InvalidOperation:
            raise ValueError("'{}' is not a decimal.".format(data))
    elif cls is text_type:
        if not isinstance(data, text_type):
            raise ValueError("'{}' is not a string.".format(data))
        d = cls(data)
    else:
        raise TypeError(
            "'{0}' is not a primitive type.".format(typing._type_repr(cls))
        )
    return d


def deserialize_optional(cls, data):
    union_types = get_union_types(cls)
    if not any(isinstance(None, ut) for ut in union_types):
        raise ValueError(cls)
    if data is None:
        return data
    for union_type in union_types:
        if isinstance(None, union_type):
            continue
        else:
            try:
                return deserialize_meta(union_type, data)
            except ValueError:
                continue
    else:
        raise ValueError()


def deserialize_meta(cls, data):
    if hasattr(cls, '__nirum_tag__') or hasattr(cls, 'Tag'):
        d = deserialize_union_type(cls, data)
    elif hasattr(cls, '__nirum_record_behind_name__'):
        d = deserialize_record_type(cls, data)
    elif (hasattr(cls, '__nirum_inner_type__') or
          hasattr(cls, '__nirum_boxed_type__')):
        # FIXME: __nirum_boxed_type__ is for backward compatibility;
        #        remove __nirum_boxed_type__ in the near future
        d = deserialize_unboxed_type(cls, data)
    elif type(cls) is typing.TupleMeta:
        # typing.Tuple dosen't have either `__origin__` and `__args__`
        # so it have to be handled special case.
        d = deserialize_tuple_type(cls, data)
    elif is_support_abstract_type(cls):
        d = deserialize_abstract_type(cls, data)
    elif is_union_type(cls):
        d = deserialize_optional(cls, data)
    elif callable(cls) and cls in _NIRUM_PRIMITIVE_TYPE:
        d = deserialize_primitive(cls, data)
    elif isinstance(cls, enum.EnumMeta):
        d = cls(data)
    else:
        raise TypeError('data is not deserializable: {!r} as {!r}'.format(
            data, cls
        ))
    return d


def deserialize_unboxed_type(cls, value):
    try:
        inner_type = cls.__nirum_inner_type__
    except AttributeError:
        # FIXME: __nirum_boxed_type__ is for backward compatibility;
        #        remove __nirum_boxed_type__ in the near future
        inner_type = cls.__nirum_boxed_type__
    deserializer = getattr(inner_type, '__nirum_deserialize__', None)
    if deserializer:
        value = deserializer(value)
    else:
        value = deserialize_meta(inner_type, value)
    return cls(value=value)


deserialize_boxed_type = deserialize_unboxed_type
# FIXME: deserialize_boxed_type() is for backward compatibility;
#        remove it in the near future


def deserialize_record_type(cls, value):
    if '_type' not in value:
        raise ValueError('"_type" field is missing.')
    if not cls.__nirum_record_behind_name__ == value['_type']:
        raise ValueError(
            '{0} expect "_type" equal to "{1.__nirum_record_behind_name__}"'
            ', but found {2}.'.format(
                typing._type_repr(cls),
                cls, value['_type']
            )
        )
    args = {}
    behind_names = cls.__nirum_field_names__.behind_names
    for attribute_name, item in value.items():
        if attribute_name == '_type':
            continue
        if attribute_name in behind_names:
            name = behind_names[attribute_name]
        else:
            name = attribute_name
        args[name] = deserialize_meta(cls.__nirum_field_types__[name], item)
    return cls(**args)


def deserialize_union_type(cls, value):
    if '_type' not in value:
        raise ValueError('"_type" field is missing.')
    if '_tag' not in value:
        raise ValueError('"_tag" field is missing.')
    if not hasattr(cls, '__nirum_tag__'):
        for sub_cls in cls.__subclasses__():
            if sub_cls.__nirum_tag__.value == value['_tag']:
                cls = sub_cls
                break
        else:
            raise ValueError(
                '{0!r} is not deserialzable tag of `{1}`.'.format(
                    value, typing._type_repr(cls)
                )
            )
    if not cls.__nirum_union_behind_name__ == value['_type']:
        raise ValueError('{0} expect "_type" equal to'
                         ' "{1.__nirum_union_behind_name__}"'
                         ', but found {2}.'.format(typing._type_repr(cls), cls,
                                                   value['_type']))
    if not cls.__nirum_tag__.value == value['_tag']:
        raise ValueError('{0} expect "_tag" equal to'
                         ' "{1.__nirum_tag__.value}"'
                         ', but found {1}.'.format(typing._type_repr(cls),
                                                   cls, value['_tag']))
    args = {}
    behind_names = cls.__nirum_tag_names__.behind_names
    for attribute_name, item in value.items():
        if attribute_name in {'_type', '_tag'}:
            continue
        if attribute_name in behind_names:
            name = behind_names[attribute_name]
        else:
            name = attribute_name
        args[name] = deserialize_meta(cls.__nirum_tag_types__[name], item)
    return cls(**args)
