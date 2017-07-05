""":mod:`nirum.serialize`
~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import datetime
import decimal
import uuid

from six import string_types

__all__ = (
    'serialize_boxed_type', 'serialize_meta',
    'serialize_record_type', 'serialize_unboxed_type',
    'serialize_union_type',
)


def serialize_unboxed_type(data):
    value = data.value
    serialize = getattr(value, '__nirum_serialize__', None)
    if callable(serialize):
        return serialize()
    else:
        return serialize_meta(value)


serialize_boxed_type = serialize_unboxed_type
# FIXME: serialize_boxed_type() is for backward compatibility;
#        remove it in the near future


def serialize_type_with_names(data, names):
    s = {}
    for slot_name in data.__slots__:
        value = getattr(data, slot_name)
        serialized_data = serialize_meta(value)
        if slot_name in names:
            behind_name = names[slot_name]
        else:
            behind_name = slot_name
        s[behind_name] = serialized_data
    return s


def serialize_record_type(data):
    s = {'_type': data.__nirum_record_behind_name__}
    s.update(serialize_type_with_names(data, data.__nirum_field_names__))
    return s


def serialize_union_type(data):
    s = {
        '_type': data.__nirum_union_behind_name__,
        '_tag': data.__nirum_tag__.value,
    }
    s.update(serialize_type_with_names(data, data.__nirum_tag_names__))
    return s


def serialize_meta(data):
    if hasattr(data, '__nirum_serialize__'):
        d = data.__nirum_serialize__()
    elif isinstance(data, (string_types, bool, int, float)):
        # FIXME: str in py2 represents binary string as well as text string.
        # It should be refactored so that the function explicitly takes
        # an expected type as like deserialize_meta() does.
        d = data
    elif (isinstance(data, datetime.datetime) or
            isinstance(data, datetime.date)):
        d = data.isoformat()
    elif isinstance(data, decimal.Decimal) or isinstance(data, uuid.UUID):
        d = str(data)
    elif (isinstance(data, collections.Set) or
          isinstance(data, collections.Sequence)):
        d = [serialize_meta(e) for e in data]
    elif isinstance(data, collections.Mapping):
        d = [
            {'key': serialize_meta(k), 'value': serialize_meta(v)}
            for k, v in data.items()
        ]
    else:
        d = data
    return d
