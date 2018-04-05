Changelog
=========

Version 0.4.3
-------------

Released on April 5, 2018.

- Added missing equality functions (i.e., ``==``, ``!=`` operators, & ``hash()``
  function) to ``nirum.datastructures.Map`` and ``nirum.datastructures.List``.
  [`#110`_]

.. _#110: https://github.com/spoqa/nirum-python/issues/110


Version 0.4.2
-------------

Released on July 6, 2017.

- Fixed a serialization bug that other set-like (i.e. ``collections.Set``) types
  than Python built-in ``set`` hadn't been reduced to simpler forms so that they
  can be encoded to JSON.
- Fixed a serialization bug that other list-like (i.e. ``collections.Sequence``)
  types than Python built-in ``list`` hadn't been reduced to simpler forms so
  that they can be encoded to JSON.



Version 0.4.1
-------------

Release on May 2, 2017.

- Compare type with its abstract type in ``nirum.validate.validate_type``.


Version 0.4.0
-------------

Release on March 20, 2017.

- Encoding of map types was changed according to the `Nirum serialization
  specification`__.  [`#66`_]
- Added ``nirum.datastructures`` module and ``nirum.datastructures.Map``
  which is an immutable dictionary.  [`#66`_]
- Added ``nirum.datastructures.List`` which is an immutable list.  [`#49`_]
- Aliased ``nirum.datastructures.Map`` as ``map_type``, and
  ``nirum.datastructures.List`` as ``list_type`` to avoid name
  conflict with user-defined types.

__ https://github.com/spoqa/nirum/blob/f1629787f45fef17eeab8b4f030c34580e0446b8/docs/serialization.md
.. _#66: https://github.com/spoqa/nirum-python/pull/66
.. _#49: https://github.com/spoqa/nirum-python/issues/49
