Changelog
=========

Version 0.4.0
-------------

Release on March 20, 2017.

- Encoding of map types was changed according to the `Nirum serialization
  specification`__.  [:issue:`66`]
- Added :mod:`nirum.datastructures` module and
  :class:`~nirum.datastructures.Map` which is an immutable dictionary.
  [:issue:`66`]
- Added :class:`nirum.datastructures.List` which is an immutable list.
  [:issue:`49`]
- Aliased :class:`~nirum.datastructures.Map` as ``map_type``, and
  :class:`~nirum.datastructures.List` as ``list_type`` to avoid name
  conflict with user-defined types.


Version 0.4.1
-------------

Release on May 2nd, 2017.

- Compare type with its abstract type in :func:`nirum.validate.validate_type`.


Version 0.4.2
-------------

To be released.


__ https://github.com/spoqa/nirum/blob/f1629787f45fef17eeab8b4f030c34580e0446b8/docs/serialization.md
