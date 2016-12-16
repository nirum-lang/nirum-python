""":mod:`nirum.rpc`
~~~~~~~~~~~~~~~~~~~

"""
import collections
import json
import typing

from six import integer_types, text_type
from six.moves import urllib
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request as WsgiRequest, Response as WsgiResponse

from .constructs import NameDict
from .deserialize import deserialize_meta
from .exc import (InvalidNirumServiceMethodNameError,
                  InvalidNirumServiceMethodTypeError,
                  NirumProcedureArgumentRequiredError,
                  NirumProcedureArgumentValueError,
                  UnexpectedNirumResponseError)
from .func import url_endswith_slash
from .serialize import serialize_meta

__all__ = 'Client', 'WsgiApp', 'Service', 'client_type', 'service_type'
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
                    "{0}.{1} inexist.".format(
                        typing._type_repr(self.__class__), method_name
                    )
                )
            if not callable(method):
                raise InvalidNirumServiceMethodTypeError(
                    "{0}.{1} isn't callable".format(
                        typing._type_repr(self.__class__), method_name
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

    def __init__(self, service):
        self.service = service

    def __call__(self, environ, start_response):
        """

        :param environ:
        :param start_response:

        """
        return self.route(environ, start_response)

    def route(self, environ, start_response):
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

    def ping(self, request, args):
        return WsgiResponse(
            '"Ok"',
            200,
            content_type='application/json'
        )

    def rpc(self, request, args):
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
                400, request,
                message="Remote procedure '{}' is not callable.".format(
                    request_method
                )
            )
        try:
            request_json = json.loads(payload)
        except ValueError:
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
        try:
            result = service_method(**arguments)
        except Exception as e:
            return self.error(500, request, str(e))
        if not self._check_return_type(type_hints['_return'], result):
            return self.error(
                400,
                request,
                message="Incorrect return type '{0}' "
                        "for '{1}'. expected '{2}'.".format(
                            typing._type_repr(result.__class__),
                            request_method,
                            typing._type_repr(type_hints['_return'])
                        )
            )
        else:
            return self._raw_response(200, serialize_meta(result))

    def _parse_procedure_arguments(self, type_hints, request_json):
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
                    "Incorrect type '{0}' for '{1}'. "
                    "expected '{2}'.".format(
                        typing._type_repr(data.__class__), behind_name,
                        typing._type_repr(type_)
                    )
                )
        return arguments

    def _check_return_type(self, type_hint, procedure_result):
        try:
            deserialize_meta(type_hint, serialize_meta(procedure_result))
        except ValueError:
            return False
        else:
            return True

    def make_error_response(self, error_type, message=None):
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

    def error(self, status_code, request, message=None):
        """Handle error response.

        :param int status_code:
        :param request:
        :return:

        """
        status_code_text = HTTP_STATUS_CODES.get(status_code, 'http error')
        status_error_tag = status_code_text.lower().replace(' ', '_')
        custom_response_map = {
            404: self.make_error_response(
                status_error_tag,
                'The requested URL {} was not found on this service.'.format(
                    request.path
                )
            ),
            400: self.make_error_response(status_error_tag, message),
            405: self.make_error_response(
                status_error_tag,
                'The requested URL {} was not allowed HTTP method {}.'.format(
                    request.path, request.method
                )
            ),
        }
        return self._raw_response(
            status_code,
            custom_response_map.get(
                status_code,
                self.make_error_response(
                    status_error_tag, message or status_code_text
                )
            )
        )

    def make_response(self, status_code, headers, content):
        return status_code, headers, content

    def _raw_response(self, status_code, response_json, **kwargs):
        response_tuple = self.make_response(
            status_code, headers=[('Content-type', 'application/json')],
            content=json.dumps(response_json).encode('utf-8')
        )
        if not isinstance(response_tuple, collections.Sequence) and \
                len(response_tuple) == 3:
            raise TypeError(
                'make_response() must return a triple of '
                '(status_code, content, headers): {}'.format(response_tuple)
            )
        status_code, headers, content = response_tuple
        if not isinstance(status_code, integer_types):
            raise TypeError(
                '`status_code` have to be instance of integer. not {}'.format(
                    typing._type_repr(type(status_code))
                )
            )
        if not isinstance(headers, collections.Sequence):
            raise TypeError(
                '`headers` have to be instance of sequence. not {}'.format(
                    typing._type_repr(type(headers))
                )
            )
        if not isinstance(content, bytes):
            raise TypeError(
                '`content` have to be instance of bytes. not {}'.format(
                    typing._type_repr(type(content))
                )
            )
        return WsgiResponse(content, status_code, headers, **kwargs)


class Client:

    def __init__(self, url, opener=urllib.request.build_opener()):
        self.url = url_endswith_slash(url)
        self.opener = opener

    def ping(self):
        req = urllib.request.Request(
            urllib.parse.urljoin(self.url, './ping/'),
            headers={'Content-Type': 'application/json;charset=utf-8',
                     'Accepts': 'application/json'}
        )
        return self.make_request(req)

    def remote_call(self, method_name, payload={}):
        qs = urllib.parse.urlencode({'method': method_name})
        scheme, netloc, path, _, _ = urllib.parse.urlsplit(self.url)
        request_url = urllib.parse.urlunsplit((
            scheme, netloc, path, qs, ''
        ))
        return self.do_request(request_url, payload)

    def make_request(self, method, request_url, headers, payload):
        return (
            method, request_url, headers, json.dumps(payload).encode('utf-8')
        )

    def do_request(self, request_url, payload):
        request_tuple = self.make_request(
            u'POST',
            request_url,
            [
                ('Content-type', 'application/json;charset=utf-8'),
                ('Accepts', 'application/json'),
            ],
            payload
        )
        if not isinstance(request_tuple, collections.Sequence) and \
                len(request_tuple) == 3:
            raise TypeError(
                'make_request() must return a triple of '
                '(status_code, content, headers): {}'.format(request_tuple)
            )
        http_method, request_url, headers, content = request_tuple
        if not isinstance(request_url, text_type):
            raise TypeError(
                '`request_url` have to be instance of text. not {}'.format(
                    typing._type_repr(type(request_url))
                )
            )
        if not isinstance(headers, collections.Sequence):
            raise TypeError(
                '`headers` have to be instance of sequence. not {}'.format(
                    typing._type_repr(type(headers))
                )
            )
        if not isinstance(content, bytes):
            raise TypeError(
                '`content` have to be instance of bytes. not {}'.format(
                    typing._type_repr(type(content))
                )
            )
        if not isinstance(http_method, text_type):
            raise TypeError(
                '`method` have to be instance of text. not {}'.format(
                    typing._type_repr(type(http_method))
                )
            )
        http_method = http_method.upper()
        proper_http_method_names = {
            'GET', 'POST', 'PUT', 'DELETE',
            'OPTIONS', 'TRACE', 'CONNECT', 'HEAD'
        }
        if http_method not in proper_http_method_names:
            raise ValueError(
                '`method` have to be one of {!r}.: {}'.format(
                    proper_http_method_names, http_method
                )
            )
        request = urllib.request.Request(request_url, data=content)
        request.get_method = lambda: http_method.upper()
        for header_name, header_content in headers:
            request.add_header(header_name, header_content)
        response = self.opener.open(request, None)
        response_text = response.read()
        if 200 <= response.status < 300:
            return response_text.decode('utf-8')
        else:
            raise UnexpectedNirumResponseError(response_text)


# To eliminate imported vars from being overridden by
# the runtime class, aliasing runtime class into lower case with underscore
# with postfix named `_type`
service_type = Service
client_type = Client
