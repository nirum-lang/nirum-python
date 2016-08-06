""":mod:`nirum.rpc`
~~~~~~~~~~~~~~~~~~~

"""
import json
import typing

from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request as WsgiRequest, Response as WsgiResponse

from .constructs import NameDict
from .deserialize import deserialize_meta
from .exc import (InvalidNirumServiceMethodNameError,
                  InvalidNirumServiceMethodTypeError,
                  NirumProcedureArgumentRequiredError,
                  NirumProcedureArgumentValueError)
from .serialize import serialize_meta

__all__ = 'WsgiApp', 'Service', 'service_type'
JSONType = typing.Mapping[
    str, typing.Union[str, float, int, bool, object]
]


class Service:
    """Nirum RPC service."""

    __nirum_service_methods__ = {}
    __nirum_method_names__ = NameDict([])

    def __init__(self):
        for method_name in self.__nirum_service_methods__:
            try:
                method = getattr(self, method_name)
            except AttributeError:
                raise InvalidNirumServiceMethodNameError(
                    "{0.__class__.__qualname__}.{1} inexist.".format(
                        self, method_name
                    )
                )
            if not callable(method):
                raise InvalidNirumServiceMethodTypeError(
                    "{0.__class__.__qualname__}.{1} isn't callable".format(
                        self, method_name
                    )
                )


class WsgiApp:
    """Create WSGI application adapt Nirum service.

    :param service: A nirum service.

    """

    #: (:class:`werkzeug.routing.Map`) url map
    url_map = Map([
        Rule('/', endpoint='rpc'),
        Rule('/ping/', endpoint='ping'),
    ])

    def __init__(self, service: Service):
        self.service = service

    def __call__(self, environ: typing.Mapping[str, object],
                 start_response: typing.Callable) -> WsgiResponse:
        """

        :param environ:
        :param start_response:

        """
        return self.route(environ, start_response)

    def route(self, environ: typing.Mapping[str, object],
              start_response: typing.Callable) -> WsgiResponse:
        """Route

        :param environ:
        :param start_response:

        """
        urls = self.url_map.bind_to_environ(environ)
        request = WsgiRequest(environ)
        try:
            endpoint, args = urls.match()
        except HTTPException as e:
            return self.error(e.code, request)(environ, start_response)
        else:
            procedure = getattr(self, endpoint)
            response = procedure(request, args)
            return response(environ, start_response)

    def ping(self, request: WsgiRequest, args: typing.Any) -> WsgiResponse:
        return WsgiResponse(
            '"Ok"',
            200,
            content_type='application/json'
        )

    def rpc(self, request: WsgiRequest, args: typing.Any) -> WsgiResponse:
        """RPC

        :param request:
        :args ???:

        """
        if request.method != 'POST':
            return self.error(405, request)
        payload = request.get_data(as_text=True) or '{}'
        request_method = request.args.get('method')
        if not request_method:
            return self.error(
                400, request,
                message="A query string parameter method= is missing."
            )
        name_map = self.service.__nirum_method_names__
        try:
            method_facial_name = name_map.behind_names[request_method]
        except KeyError:
            return self.error(
                400,
                request,
                message="Service dosen't have procedure named '{}'.".format(
                    request_method
                )
            )
        try:
            service_method = getattr(self.service, method_facial_name)
        except AttributeError:
            return self.error(
                400,
                request,
                message="Service has no procedure '{}'.".format(
                    request_method
                )
            )
        if not callable(service_method):
            return self.error(
                400,
                request,
                message="Remote procedure '{}' is not callable.".format(
                    request_method
                )
            )
        try:
            request_json = json.loads(payload)
        except json.decoder.JSONDecodeError:
            return self.error(
                400,
                request,
                message="Invalid JSON payload: '{}'.".format(payload)
            )
        type_hints = self.service.__nirum_service_methods__[method_facial_name]
        try:
            arguments = self._parse_procedure_arguments(
                type_hints,
                request_json
            )
        except (NirumProcedureArgumentValueError,
                NirumProcedureArgumentRequiredError) as e:
            return self.error(400, request, message=str(e))
        result = service_method(**arguments)
        if not self._check_return_type(type_hints['_return'], result):
            return self.error(
                400,
                request,
                message="Incorrect return type '{0.__class__.__qualname__}' "
                        "for '{1}'. expected '{2.__qualname__}'.".format(
                            result, request_method, type_hints['_return']
                        )
            )
        else:
            return self._json_response(200, result)

    def _parse_procedure_arguments(
        self,
        type_hints: typing.Mapping[str, typing.Union[type, NameDict]],
        request_json: JSONType
    ) -> typing.Mapping[str, typing.Union[str, float, int, bool, object]]:
        arguments = {}
        name_map = type_hints['_names']
        for argument_name, type_ in type_hints.items():
            if argument_name.startswith('_'):
                continue
            behind_name = name_map[argument_name]
            try:
                data = request_json[behind_name]
            except KeyError:
                raise NirumProcedureArgumentRequiredError(
                    "A argument named '{}' is missing, it is required.".format(
                        behind_name
                    )
                )
            try:
                arguments[argument_name] = deserialize_meta(type_, data)
            except ValueError:
                raise NirumProcedureArgumentValueError(
                    "Incorrect type '{0.__class__.__name__}' for '{1}'. "
                    "expected '{2.__name__}'.".format(
                        data, behind_name, type_
                    )
                )
        return arguments

    def _check_return_type(
        self,
        type_hint: type, procedure_result: typing.Any
    ) -> bool:
        try:
            deserialize_meta(type_hint, serialize_meta(procedure_result))
        except ValueError:
            return False
        else:
            return True

    def _make_error_response(
        self, error_type: str, message: typing.Optional[str]=None
    ) -> typing.Mapping[str, str]:
        """Create error response json temporary.

        .. code-block:: nirum

           union error
               = not-found (text message)
               | bad-request (text message)
               | ...

        """
        # FIXME error response has to be generated from nirum core.
        return {
            '_type': 'error',
            '_tag': error_type,
            'message': message,
        }

    def error(
        self, status_code: int, request: WsgiRequest,
        *, message: typing.Optional[str]=None
    ) -> WsgiResponse:
        """Handle error response.

        :param int status_code:
        :param request:
        :return:

        """
        status_code_text = HTTP_STATUS_CODES.get(status_code, 'http error')
        status_error_tag = status_code_text.lower().replace(' ', '_')
        custom_response_map = {
            404: self._make_error_response(
                status_error_tag,
                'The requested URL {} was not found on this service.'.format(
                    request.path
                )
            ),
            400: self._make_error_response(status_error_tag, message),
            405: self._make_error_response(
                status_error_tag,
                'The requested URL {} was not allowed HTTP method {}.'.format(
                    request.path, request.method
                )
            ),
        }
        return self._json_response(
            status_code,
            custom_response_map.get(
                status_code, self._make_error_response(status_error_tag,
                                                       status_code_text)
            )
        )

    def _json_response(
        self, status_code: int, response_json: JSONType, **kwargs
    ) -> WsgiResponse:
        return WsgiResponse(
            json.dumps(response_json),
            status_code,
            content_type='application/json',
            **kwargs
        )


# To eliminate imported vars from being overridden by
# the runtime class, aliasing runtime class into lower case with underscore
# with postfix named `_type`
service_type = Service
