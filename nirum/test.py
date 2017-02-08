import socket

from six import PY3
from six.moves import urllib
from six.moves.http_client import HTTPResponse
from werkzeug.test import Client
from werkzeug.wrappers import Response
from werkzeug.wsgi import DispatcherMiddleware

from .func import url_endswith_slash
from .rpc import WsgiApp

__all__ = 'MockHttpResponse', 'MockOpener'


class MockHttpResponse(HTTPResponse):

    def __init__(self, body, status_code):
        self.body = body
        self.code = status_code
        if PY3:
            self.status = status_code

    def read(self):
        return self.body.encode('utf-8')


class MockOpener(urllib.request.OpenerDirector):

    def __init__(self, url, service_impl_cls):
        self.url = url_endswith_slash(url)
        self.scheme, self.host, self.path, _, _ = urllib.parse.urlsplit(
            self.url
        )

        def null_app(environ, start_response):
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return ['Not Found']

        wsgi_app = WsgiApp(service_impl_cls())
        if self.path != '/':
            self.wsgi_app = DispatcherMiddleware(
                null_app, {self.path[:-1]: wsgi_app}
            )
        else:
            self.wsgi_app = wsgi_app
        self.wsgi_test_client = Client(self.wsgi_app, Response)

    def open(self, fullurl, data, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        if isinstance(fullurl, str):
            req = urllib.request.Request(fullurl, data=data)
        else:
            req = fullurl
        scheme, host, path, qs, _ = urllib.parse.urlsplit(req.get_full_url())
        assert self.scheme == scheme
        assert self.host == host
        assert self.path == path
        path_only = urllib.parse.urlunsplit(('', '', path, qs, ''))
        request_func = getattr(self.wsgi_test_client, req.get_method().lower())
        wsgi_response = request_func(
            path_only, data=req.data, headers=req.headers
        )
        return MockHttpResponse(
            wsgi_response.get_data(as_text=True),
            wsgi_response.status_code
        )
