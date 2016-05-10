""":mod:`nirum.validate`
~~~~~~~~~~~~~~~~~~~~~~~~

"""
__all__ = 'validate_boxed_type',


def validate_boxed_type(boxed, type_hint) -> bool:
    if not isinstance(boxed, type_hint):
        raise TypeError('{0} expected, found: {1}'.format(type_hint,
                                                          type(boxed)))
    return True
