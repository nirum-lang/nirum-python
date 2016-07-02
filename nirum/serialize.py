""":mod:`nirum.serialize`
~~~~~~~~~~~~~~~~~~~~~~~~~

"""
__all__ = (
    'serialize_boxed_type', 'serialize_record_type',
    'serialize_union_type',
)


def serialize_boxed_type(data):
    try:
        serialize_data = data.value.__nirum_serialize__()
    except AttributeError:
        serialize_data = data.value
    finally:
        return serialize_data


def serialize_type_with_names(data, names):
    s = {}
    for slot_name in data.__slots__:
        value = getattr(data, slot_name)
        try:
            serialized_data = value.__nirum_serialize__()
        except AttributeError:
            serialized_data = value
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
