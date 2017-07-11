""":mod:`nirum.transport` --- Transport interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
__all__ = 'Transport',


class Transport(object):

    def __init__(self, url):
        self.url = url

    def call(self,
             method_name,
             payload,
             service_annotations,
             method_annotations,
             parameter_annotations):
        """Call the method of the service.

        :param method_name: A normalized behind name of the method to
                            call.  See also `Nirum's serialization format
                            docs <serialization-format>`_.
        :type method_name: :class:`str`
        :param paylaod: A mapping of parameter names to serialized argument
                        values.  The keys have to be normalized behind names
                        of parameters.  The values have to be serialized
                        argument values.  See also `Nirum's serialization
                        format docs <serialization-format>`_.
        :type payload: :class:`~typing.Mapping`\ [:class:`str`,
            :class:`~typing.Union`\ [:class:`~typing.Mapping`,
            :class:`~typing.Sequence`, :class:`int`, :class:`float`,
            :class:`bool`, :const:`None`]]
        :param service_annotations: A mapping of annotations of the service.
            The keys are normalized behind names of annotations.
            The values are annotation value strings or :const:`None`
            if an annotation has no value.
        :type service_annotations: :class:`~typing.Mapping`\ [:class:`str`,
            :class:`~typing.Optional`\ [:class:`str`]]
        :param method_annotations: A mapping of annotations of the method.
            The keys are normalized behind names of annotations.
            The values are annotation value strings or :const:`None`
            if an annotation has no value.
        :type method_annotations: :class:`~typing.Mapping`\ [:class:`str`,
            :class:`~typing.Optional`\ [:class:`str`]]
        :param parameter_annotations: A mapping of parameter annotations.
            Its structure is similar to ``service_annotations`` and
            ``method_annotations`` except it's one more level nested.
            The keys are normalized behind names of parameters.
            The values are the annotation mappings of their corresponding
            parameter.
        :type parameter_annotations: :class:`~typing.Mapping`\ [:class:`str`,
            :class:`~typing.Mapping`\ [:class:`str`,
            :class:`~typing.Optional`\ [:class:`str`]]]
        :return: A pair of the method result.  The first arity is a
                 :class:`bool` value which represents whether the call
                 is successful, and the second arity is a serialized
                 return value (if it's successful) or error value
                 (if it's not successful).  The responsibility of
                 deserializing the result value is caller's.
        :rtype: :class:`~typing.Tuple`\ [:class:`bool`,
            :class:`~typing.Union`\ [:class:`~typing.Mapping`,
            :class:`~typing.Sequence`, :class:`int`, :class:`float`,
            :class:`bool`, :const:`None`]]

        .. note::

           Every transport has to implement this method.

        .. _serialization-format: \
https://github.com/spoqa/nirum/blob/master/docs/serialization.md

        """
        raise NotImplementedError('Transport has to implement call() method')

    def __call__(self,
                 method_name,
                 payload,
                 service_annotations,
                 method_annotations,
                 parameter_annotations):
        return self.call(
            method_name,
            payload,
            service_annotations,
            method_annotations,
            parameter_annotations
        )
