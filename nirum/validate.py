""":mod:`nirum.validate`
~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import typing

from ._compat import get_abstract_param_types, get_union_types, is_union_type

__all__ = (
    'validate_boxed_type', 'validate_record_type', 'validate_type',
    'validate_unboxed_type', 'validate_union_type',
)


def validate_type(data, type_):
    instance_check = False
    abstract_types = {typing.AbstractSet, typing.Sequence, typing.Mapping}
    if hasattr(type_, '__origin__') and type_.__origin__ in abstract_types:
        param_type = get_abstract_param_types(type_)
        imp_types = {
            typing.AbstractSet: set,
            typing.Sequence: list,
            typing.Mapping: collections.Mapping,
        }
        instance_check = isinstance(data, imp_types[type_.__origin__]) and \
            all(isinstance(item, param_type[0]) for item in data)
    else:
        try:
            instance_check = isinstance(data, type_)
        except TypeError:
            if is_union_type(type_):
                instance_check = any(
                    isinstance(data, t) for t in get_union_types(type_)
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
