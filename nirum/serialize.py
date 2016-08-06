""":mod:`nirum.serialize`
~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import datetime
import decimal
import uuid

__all__ = (
    'serialize_boxed_type', 'serialize_meta',
    'serialize_record_type', 'serialize_union_type',
)


def serialize_boxed_type(data):
    value = data.value
    serialize = getattr(value, '__nirum_serialize__', None)
    if callable(serialize):
        return serialize()
    return value


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
    elif type(data) in {str, float, bool, int}:
        d = data
    elif (isinstance(data, datetime.datetime) or
            isinstance(data, datetime.date)):
        d = data.isoformat()
    elif isinstance(data, decimal.Decimal) or isinstance(data, uuid.UUID):
        d = str(data)
    elif isinstance(data, set):
        d = sorted(serialize_meta(e) for e in data)
    elif isinstance(data, list):
        d = [serialize_meta(e) for e in data]
    elif isinstance(data, dict):
        d = {
            k: serialize_meta(v)
            for k, v in data.items()
        }
    else:
        d = data
    return d
