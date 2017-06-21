Changelog
=========

Version 0.5.2
-------------

To be released.


Version 0.5.1
-------------

Released on June 22, 2017.

- Added Python 3.6 support.
- Fixed a bug that service client methods hadn't raised the proper error
  type but ``nirum.exc.UnexpectedNirumResponseError`` instead.  [`#71`_]
- Wheel distributions (``nirum-*.whl``) are now universal between Python 2
  and 3.  [`#78`_]
- ``nirum.rpc.Service`` had been an old-style class on Python 2, but now
  it became a new-style class also on Python 2.  (As Python 3 has only new-style
  class, there's no change on Python 3.)  [`#83`_]
- ``nirum.rpc.Client`` and its subtype became to raise ``TypeError`` with
  a better error message when its ``make_request()`` method is overridden and
  it returns a wrong artity of tuple.  [`#80`_]
- ``nirum.rpc.WsgiApp`` and its subtype became to raise ``TypeError`` with
  a better error message when its ``make_response()`` method is overridden and
  it returns a wrong artity of tuple.  [`#80`_]
- Fixed a bug that ``Client.ping()`` method had always raised ``TypeError``.
  [`#80`_]
- Corrected a typo ``Accepts`` on request headers ``Client`` makes to
  ``Accept``.

.. _#78: https://github.com/spoqa/nirum-python/pull/78
.. _#83: https://github.com/spoqa/nirum-python/issues/83
.. _#80: https://github.com/spoqa/nirum-python/pull/80


Version 0.5.0
-------------

Released on June 1, 2017.

- Service methods became able to specify its error type. [`#71`_]
- Added ``nirum-server`` command to run simply Nirum service.

.. _#71: https://github.com/spoqa/nirum-python/issues/71


Version 0.4.1
-------------

Released on May 2, 2017.

- Compare type with its abstract type in ``nirum.validate.validate_type``.


Version 0.4.0
-------------

Released on March 20, 2017.

- Encoding of map types was changed according to the `Nirum serialization
  specification`__.  [`#66`_]
- Added ``nirum.datastructures`` module and ``nirum.datastructures.Map``
  which is an immutable dictionary.  [`#66`_]
- Added ``nirum.datastructures.List`` which is an immutable list.
  [`#49`_]
- Aliased ``nirum.datastructures.Map`` as ``map_type``, and
  ``nirum.datastructures.List`` as ``list_type`` to avoid name
  conflict with user-defined types.

.. _#66: https://github.com/spoqa/nirum-python/pull/66
.. _#49: https://github.com/spoqa/nirum-python/issues/49
__ https://github.com/spoqa/nirum/blob/f1629787f45fef17eeab8b4f030c34580e0446b8/docs/serialization.md
