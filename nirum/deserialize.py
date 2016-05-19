""":mod:`nirum.deserialize`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
__all__ = 'deserialize_boxed_type', 'deserialize_record_type'


def deserialize_boxed_type(cls, value):
    return cls(value=value)


def deserialize_record_type(cls, values):
    if '_type' not in values:
        raise ValueError('"_type" field is missing.')
    if not cls.__nirum_record_behind_name__ == values['_type']:
        raise ValueError('{0.__class__.__name__} expect "_type" equal to'
                         ' "{0.__nirum_record_behind_name__}"'
                         ', but found {1}.'.format(cls, values['_type']))
    args = {}
    behind_names = cls.__nirum_field_names__.behind_names
    for attribute_name, value in values.items():
        if attribute_name == '_type':
            continue
        if attribute_name in behind_names:
            args[behind_names[attribute_name]] = value
        else:
            args[attribute_name] = value
    return cls(**args)
