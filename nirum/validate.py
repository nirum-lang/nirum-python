""":mod:`nirum.validate`
~~~~~~~~~~~~~~~~~~~~~~~~

"""
__all__ = 'validate_boxed_type', 'validate_record_type', 'validate_union_type',


def validate_boxed_type(boxed, type_hint) -> bool:
    if not isinstance(boxed, type_hint):
        raise TypeError('{0} expected, found: {1}'.format(type_hint,
                                                          type(boxed)))
    return boxed


def validate_record_type(record):
    for attr, type_ in record.__nirum_field_types__.items():
        data = getattr(record, attr)
        if not isinstance(data, type_):
            raise TypeError(
                'expect {0.__class__.__name__}.{1} to be {2}'
                ', but found: {3}'.format(record, attr, type_, type(data))
            )
    else:
        return record


def validate_union_type(union):
    for attr, type_ in union.__nirum_tag_types__.items():
        data = getattr(union, attr)
        if not isinstance(data, type_):
            raise TypeError(
                'expect {0.__class__.__name__}.{1} to be {2}'
                ', but found: {3}'.format(union, attr, type_, type(data))
            )
    else:
        return union
