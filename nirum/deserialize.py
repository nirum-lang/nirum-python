""":mod:`nirum.deserialize`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
__all__ = 'deserialize_boxed_type',


def deserialize_boxed_type(cls, value):
    return cls(value=value)
