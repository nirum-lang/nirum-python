""":mod:`nirum.deserialize`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
__all__ = (
    'deserialize_boxed_type', 'deserialize_meta',
    'deserialize_record_type', 'deserialize_union_type',
)


def deserialize_meta(cls, data):
    if not isinstance(data, dict):
        d = cls(data)
    elif '_type' in data and '_tag' in data:
        d = deserialize_union_type(cls, data)
    elif '_type' in data:
        d = deserialize_record_type(cls, data)
    else:
        raise TypeError('data is not deserializable: {!r}'.format(data))
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
