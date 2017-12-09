Changelog
=========

Version 0.6.2
-------------

To be released.


Version 0.6.1
-------------

Released on December 9, 2017.

- Made `nirum.datastructures.List` to copy the given value so that
  it doesn't refer given value's state and is immutable.


Version 0.6.0
-------------

Released on July 11, 2017.

- Deprecated ``nirum.rpc`` module.

  This module and all it has provided are deprecated or obsolete.  The most
  of them are now distributed as separated packages, or replaced by a newer
  concept.  See also the below for details.

  It will be completely obsolete at version 0.7.0.

- Client transport layer.  [`#79`_]

  - Added ``nirum.transport.Transport`` interface.

    The recent builds of Nirum compiler became to generate ``*_Client`` classes
    taking a ``nirum.transport.Transport`` instance through their constructor.

    Use nirum-python-http_ (PyPI handle: ``nirum-http``) instead for HTTP
    client of services e.g.:

    .. code-block:: python

       from yourservice import YourService_Client
       from nirum_http import HttpTransport

       transport = HttpTransport('https://service-host/')
       client = YourService_Client(transport)

  - Deprecated ``nirum.rpc.Client`` type.  The recent builds of Nirum compiler
    became to generate ``*_Client`` classes for services without subclassing
    ``nirum.rpc.Client``.

    The deprecated ``nirum.rpc.Client`` will be completely obsolete at
    version 0.7.0.

- ``nirum.rpc.Service`` was moved to ``nirum.service.Service``.

  The recent builds of Nirum compiler became to generate service classes
  that inherit ``nirum.service.Service`` instead of ``nirum.rpc.Service``.

  The deprecated ``nirum.rpc.Service`` will be completely obsolete at
  version 0.7.0.

- Deprecated ``nirum.rpc.WsgiApp``.  This will be completely obsolete at
  version 0.7.0.

  Use nirum-python-wsgi_ (PyPI handle: ``nirum-wsgi``) instead.

- ``nirum-server`` command is obsolete.  The same command is now provided
  by nirum-python-wsgi_ (PyPI handle: ``nirum-wsgi``), a separated package.

- ``nirum.func.import_string()`` function and ``nirum.func.IMPORT_RE`` constant
  are obsolete.

- Fixed ``NameError`` raised from forward references.  [`compiler #138`_]

.. _#79: https://github.com/spoqa/nirum-python/issues/79
.. _compiler #138: https://github.com/spoqa/nirum/issues/138
.. _nirum-python-http: https://github.com/spoqa/nirum-python-http
.. _nirum-python-wsgi: https://github.com/spoqa/nirum-python-wsgi


Version 0.5.4
-------------

Released on December 9, 2017.

- Made `nirum.datastructures.List` to copy the given value so that
  it doesn't refer given value's state and is immutable.


Version 0.5.3
-------------

Released on July 6, 2017.

- Fixed a serialization bug that other set-like (i.e. ``collections.Set``) types
  than Python built-in ``set`` hadn't been reduced to simpler forms so that they
  can be encoded to JSON.
- Fixed a serialization bug that other list-like (i.e. ``collections.Sequence``)
  types than Python built-in ``list`` hadn't been reduced to simpler forms so
  that they can be encoded to JSON.


Version 0.5.2
-------------

Released on June 23, 2017.

- ``url`` of ``nirum.rpc.Client`` and
  ``method`` of ``nirum.rpc.Client.make_request``
  now can be both ``unicode`` and ``str`` on Python 2.7. [`#87`_]
- ``nirum.rpc.Client`` had been an old-style class on Python 2, but now
  it became a new-style class also on Python 2. (As Python 3 has only new-style
  class, there's no change on Python 3.)

.. _#87: https://github.com/spoqa/nirum-python/pull/87


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
