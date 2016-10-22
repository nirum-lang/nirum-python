""":mod:`nirum.validate`
~~~~~~~~~~~~~~~~~~~~~~~~

"""
import typing

__all__ = (
    'validate_boxed_type', 'validate_record_type', 'validate_type',
    'validate_unboxed_type', 'validate_union_type',
)


def validate_type(data, type_):
    instance_check = False
    try:
        instance_check = isinstance(data, type_)
    except TypeError:
        if type(type_) is typing.UnionMeta:
            instance_check = any(
                isinstance(data, t) for t in type_.__union_params__
            )
        else:
            raise ValueError('{!r} cannot validated.'.format(type_))
    return instance_check


def validate_unboxed_type(unboxed, type_hint):
    if not isinstance(unboxed, type_hint):
        raise TypeError('{0} expected, found: {1}'.format(type_hint,
                                                          type(unboxed)))
    return unboxed


validate_boxed_type = validate_unboxed_type
# FIXME: validate_boxed_type() is for backward compatibility;
#        remove it in the near future


def validate_record_type(record):
    for attr, type_ in record.__nirum_field_types__.items():
        data = getattr(record, attr)
        if not validate_type(data, type_):
            raise TypeError(
                'expect {0}.{1} to be {2}'
                ', but found: {3}'.format(typing._type_repr(record.__class__),
                                          attr, type_, type(data))
            )
    else:
        return record


def validate_union_type(union):
    for attr, type_ in union.__nirum_tag_types__.items():
        data = getattr(union, attr)
        if not validate_type(data, type_):
            raise TypeError(
                'expect {0}.{1} to be {2}'
                ', but found: {3}'.format(typing._type_repr(union.__class__),
                                          attr, type_, type(data))
            )
    else:
        return union
