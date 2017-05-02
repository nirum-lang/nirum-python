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
- Compare type with its abstract type in :func:`nirum.validate.validate_type`.

__ https://github.com/spoqa/nirum/blob/f1629787f45fef17eeab8b4f030c34580e0446b8/docs/serialization.md
