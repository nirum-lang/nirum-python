""":mod:`nirum.serialize`
~~~~~~~~~~~~~~~~~~~~~~~~~

"""
__all__ = 'serialize_boxed_type', 'serialize_record_type'


def serialize_boxed_type(data):
    return data.value


def serialize_record_type(data):
    s = {'_type': data.__nirum_record_behind_name__}
    for slot_name in data.__slots__:
        value = getattr(data, slot_name)
        try:
            serialized_data = value.__nirum_serialize__()
        except AttributeError:
            serialized_data = value
        if slot_name in data.__nirum_field_names__:
            behind_name = data.__nirum_field_names__[slot_name]
        else:
            behind_name = slot_name
        s[behind_name] = serialized_data
    return s
