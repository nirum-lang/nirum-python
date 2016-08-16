""":mod:`nirum.deserialize`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import datetime
import decimal
import enum
import typing
import uuid

from iso8601 import iso8601, parse_date

__all__ = (
    'deserialize_abstract_type',
    'deserialize_boxed_type',
    'deserialize_iterable_abstract_type',
    'deserialize_meta',
    'deserialize_optional',
    'deserialize_primitive',
    'deserialize_record_type',
    'deserialize_tuple_type',
    'deserialize_union_type',
    'is_support_abstract_type',
)
_NIRUM_PRIMITIVE_TYPE = {
    str, float, decimal.Decimal, uuid.UUID, datetime.datetime,
    datetime.date, bool, int
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
        typing.Mapping,
        typing.Dict,
    }
    return any(type_ is data_type for type_ in abstract_types)


def deserialize_iterable_abstract_type(cls, cls_origin_type, data):
    abstract_type_map = {
        typing.Sequence: list,
        typing.List: list,
        typing.Set: set,
    }
    deserialized_data = data
    cls_primitive_type = abstract_type_map[cls_origin_type]
    if isinstance(cls.__parameters__[0], typing.TypeVar):
        deserialized_data = cls_primitive_type(data)
    else:
        deserialized_data = cls_primitive_type(
            deserialize_meta(cls.__parameters__[0], d) for d in data
        )
    return deserialized_data


def deserialize_abstract_type(cls, data):
    abstract_type_map = {
        typing.Sequence: list,
        typing.List: list,
        typing.Mapping: dict,
        typing.Dict: dict,
        typing.Set: set,
    }
    cls_origin_type = cls.__origin__
    if cls_origin_type is None:
        cls_origin_type = cls
    iterable_types = {typing.Sequence, typing.List, typing.Tuple, typing.Set}
    if cls_origin_type in iterable_types:
        return deserialize_iterable_abstract_type(cls, cls_origin_type, data)
    else:
        return abstract_type_map[cls_origin_type](data)


def deserialize_tuple_type(cls, data):
    if not cls.__tuple_params__:
        return tuple(data)
    if len(cls.__tuple_params__) != len(data):
        raise ValueError(
            'Expected {}-tuple, not {}-tuple'.format(
                len(cls.__tuple_params__), len(data)
            )
        )
    return tuple(
        deserialize_meta(t, d)
        for t, d in zip(cls.__tuple_params__, data)
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
    elif cls is decimal.Decimal:
        try:
            d = cls(data)
        except decimal.InvalidOperation:
            raise ValueError("'{}' is not a decimal.".format(data))
    elif cls is str:
        if not isinstance(data, str):
            raise ValueError("'{}' is not a string.")
        d = cls(data)
    else:
        raise TypeError(
            "'{0.__qualname__}' is not a primitive type.".format(cls)
        )
    return d


def deserialize_optional(cls, data):
    if not any(isinstance(None, ut) for ut in cls.__union_params__):
        raise ValueError(cls)
    if data is None:
        return data
    for union_type in cls.__union_params__:
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
    if hasattr(cls, '__nirum_tag__'):
        d = deserialize_union_type(cls, data)
    elif hasattr(cls, '__nirum_record_behind_name__'):
        d = deserialize_record_type(cls, data)
    elif hasattr(cls, '__nirum_boxed_type__'):
        d = deserialize_boxed_type(cls, data)
    elif type(cls) is typing.TupleMeta:
        # typing.Tuple dosen't have either `__origin__` and `__parameters__`
        # so it have to be handled special case.
        d = deserialize_tuple_type(cls, data)
    elif is_support_abstract_type(cls):
        d = deserialize_abstract_type(cls, data)
    elif type(cls) is typing.UnionMeta:
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


def deserialize_boxed_type(cls, value):
    deserializer = getattr(cls.__nirum_boxed_type__,
                           '__nirum_deserialize__', None)
    if deserializer:
        value = deserializer(value)
    return cls(value=value)


def deserialize_record_type(cls, value):
    if '_type' not in value:
        raise ValueError('"_type" field is missing.')
    if not cls.__nirum_record_behind_name__ == value['_type']:
        raise ValueError('{0.__class__.__name__} expect "_type" equal to'
                         ' "{0.__nirum_record_behind_name__}"'
                         ', but found {1}.'.format(cls, value['_type']))
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
    if not cls.__nirum_union_behind_name__ == value['_type']:
        raise ValueError('{0.__class__.__name__} expect "_type" equal to'
                         ' "{0.__nirum_union_behind_name__}"'
                         ', but found {1}.'.format(cls, value['_type']))
    if not cls.__nirum_tag__.value == value['_tag']:
        raise ValueError('{0.__class__.__name__} expect "_tag" equal to'
                         ' "{0.__nirum_tag__.value}"'
                         ', but found {1}.'.format(cls, value['_tag']))
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
