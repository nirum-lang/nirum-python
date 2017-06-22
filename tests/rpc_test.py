import json

from pytest import fixture, raises, mark
from six import text_type
from werkzeug.test import Client as TestClient
from werkzeug.wrappers import Response

from .nirum_schema import import_nirum_fixture
from nirum.exc import (InvalidNirumServiceMethodTypeError,
                       InvalidNirumServiceMethodNameError)
from nirum.rpc import Client, WsgiApp
from nirum.test import MockOpener


nf = import_nirum_fixture()


class MusicServiceImpl(nf.MusicService):

    music_map = {
        u'damien rice': [u'9 crimes', u'Elephant'],
        u'ed sheeran': [u'Thinking out loud', u'Photograph'],
    }

    def get_music_by_artist_name(self, artist_name):
        if artist_name == 'error':
            raise nf.Unknown()
        elif artist_name not in self.music_map:
            raise nf.BadRequest()
        return self.music_map.get(artist_name)

    def incorrect_return(self):
        return 1

    def get_artist_by_music(self, music):
        for k, v in self.music_map.items():
            if music in v:
                return k
        return u'none'

    def raise_application_error_request(self):
        raise ValueError('hello world')


class MusicServiceNameErrorImpl(nf.MusicService):

    __nirum_service_methods__ = {
        'foo': {'_v': 2}
    }


class MusicServiceTypeErrorImpl(nf.MusicService):

    get_music_by_artist_name = 1


class MethodClient(Client):

    def __init__(self, method, url, opener):
        self.method = method
        super(MethodClient, self).__init__(url, opener)

    def make_request(self, _, request_url, headers, payload):
        return (
            self.method, request_url, headers,
            json.dumps(payload).encode('utf-8')
        )


@mark.parametrize('impl, error_class', [
    (MusicServiceNameErrorImpl, InvalidNirumServiceMethodNameError),
    (MusicServiceTypeErrorImpl, InvalidNirumServiceMethodTypeError),
])
def test_service(impl, error_class):
    with raises(error_class):
        impl()


@fixture
def fx_music_wsgi():
    return WsgiApp(MusicServiceImpl())


@fixture
def fx_test_client(fx_music_wsgi):
    return TestClient(fx_music_wsgi, Response)


def test_wsgi_app_ping(fx_music_wsgi, fx_test_client):
    assert fx_music_wsgi.service
    response = fx_test_client.get('/ping/')
    data = json.loads(response.get_data(as_text=True))
    assert 'Ok' == data


def assert_response(response, status_code, expect_json):
    assert response.status_code == status_code, response.get_data(as_text=True)
    actual_response_json = json.loads(
        response.get_data(as_text=True)
    )
    assert actual_response_json == expect_json


def test_wsgi_app_error(fx_test_client):
    # method not allowed
    assert_response(
        fx_test_client.get('/?method=get_music_by_artist_name'),
        405,
        {
            '_type': 'error',
            '_tag': 'method_not_allowed',
            'message': 'The requested URL / was not allowed HTTP method GET.'

        }
    )
    # method missing
    assert_response(
        fx_test_client.post('/'),
        400,
        {
            '_type': 'error',
            '_tag': 'bad_request',
            'message': "A query string parameter method= is missing."

        }
    )
    # invalid procedure name
    assert_response(
        fx_test_client.post('/?method=foo'),
        400,
        {
            '_type': 'error',
            '_tag': 'bad_request',
            'message': "Service dosen't have procedure named 'foo'."

        }
    )
    # invalid json
    assert_response(
        fx_test_client.post(
            '/?method=get_music_by_artist_name', data="!",
            content_type='application/json'
        ),
        400,
        {
            '_type': 'error',
            '_tag': 'bad_request',
            'message': "Invalid JSON payload: '!'."

        }
    )
    # incorrect return
    assert_response(
        fx_test_client.post('/?method=incorrect_return'),
        400,
        {
            '_type': 'error',
            '_tag': 'bad_request',
            'message': "Incorrect return type 'int' for 'incorrect_return'. "
                       "expected '{}'.".format(text_type.__name__)
        }
    )


def test_procedure_bad_request(fx_test_client):
    assert_response(
        fx_test_client.post('/?method=get_music_by_artist_name'),
        400,
        {
            '_type': 'error',
            '_tag': 'bad_request',
            'message': "A argument named 'artist_name' is missing, "
                       "it is required.",
        }
    )
    payload = {
        'artist_name': 1
    }
    assert_response(
        fx_test_client.post(
            '/?method=get_music_by_artist_name',
            data=json.dumps(payload),
            content_type='application/json'
        ),
        400,
        {
            '_type': 'error',
            '_tag': 'bad_request',
            'message': "Incorrect type 'int' for 'artist_name'. "
                       "expected '{}'.".format(text_type.__name__)
        }
    )


@mark.parametrize(
    'payload, expected_json',
    [
        ({'artist_name': u'damien rice'}, [u'9 crimes', u'Elephant']),
        (
            {'artist_name': u'ed sheeran'},
            [u'Thinking out loud', u'Photograph']
        ),
    ]
)
def test_wsgi_app_method(fx_test_client, payload, expected_json):
    response = fx_test_client.post(
        '/?method=get_music_by_artist_name',
        data=json.dumps(payload),
        content_type='application/json'
    )
    data = json.loads(response.get_data(as_text=True))
    assert data == expected_json


def test_wsgi_app_http_error(fx_test_client):
    response = fx_test_client.post('/foobar')
    assert response.status_code == 404
    response_json = json.loads(response.get_data(as_text=True))
    assert response_json == {
        '_type': 'error',
        '_tag': 'not_found',
        'message': 'The requested URL /foobar was not found on this service.',
    }


def test_wsgi_app_with_behind_name(fx_test_client):
    payload = {'norae': u'9 crimes'}
    assert_response(
        fx_test_client.post(
            '/?method=get_artist_by_music',
            data=json.dumps(payload),
            content_type='application/json'
        ),
        400,
        {
            '_type': 'error',
            '_tag': 'bad_request',
            'message': "Service dosen't have procedure named "
                       "'get_artist_by_music'."

        }
    )
    assert_response(
        fx_test_client.post(
            '/?method=find_artist',
            data=json.dumps({'music': '9 crimes'}),
            content_type='application/json'
        ),
        400,
        {
            '_type': 'error',
            '_tag': 'bad_request',
            'message': "A argument named 'norae' is missing, "
                       "it is required.",
        }
    )
    assert_response(
        fx_test_client.post(
            '/?method=find_artist',
            data=json.dumps(payload),
            content_type='application/json'
        ),
        200,
        u'damien rice'
    )


@mark.parametrize('arity', [0, 1, 2, 4])
def test_wsgi_app_make_response_arity_check(arity):
    class ExtendedWsgiApp(WsgiApp):
        def make_response(self, status_code, headers, content):
            return (status_code, headers, content, None)[:arity]
    wsgi_app = ExtendedWsgiApp(MusicServiceImpl())
    client = TestClient(wsgi_app, Response)
    with raises(TypeError) as e:
        client.post('/?method=get_music_by_artist_name',
                    data=json.dumps({'artist_name': u'damien rice'}))
    assert str(e.value).startswith('make_response() must return a triple of '
                                   '(status_code, headers, content), not ')


@mark.parametrize('url, expected_url', [
    (u'http://foobar.com', u'http://foobar.com/'),
    (u'http://foobar.com/', u'http://foobar.com/'),
    (u'http://foobar.com?a=1#a', u'http://foobar.com/'),
    (u'http://foobar.com/?a=1#a', u'http://foobar.com/'),
])
def test_rpc_client(url, expected_url):
    assert Client(url).url == expected_url


@mark.parametrize('url', ['adfoj', 'http://'])
def test_rpc_client_error(url):
    with raises(ValueError):
        Client(url)


@mark.parametrize('url', [u'http://foobar.com/', u'http://foobar.com/rpc/'])
def test_rpc_client_service(url):
    client = nf.MusicService_Client(url, MockOpener(url, MusicServiceImpl))
    nine_crimes = '9 crimes'
    damien_music = [nine_crimes, 'Elephant']
    damien_rice = 'damien rice'
    assert client.get_music_by_artist_name(damien_rice) == damien_music
    assert client.get_artist_by_music(nine_crimes) == damien_rice


def test_rpc_mock_opener_null_app():
    url = u'http://foobar.com/rpc/'
    client = nf.MusicService_Client(url, MockOpener(url, MusicServiceImpl))
    response = client.opener.wsgi_test_client.post('/')
    assert response.status_code == 404


@mark.parametrize('method_name', ['POST', 'post'])
def test_rpc_client_make_request(method_name):
    naver = u'http://naver.com'
    payload = {'hello': 'world'}
    client = nf.MusicService_Client(naver, MockOpener(naver, MusicServiceImpl))
    actual_method, request_url, header, actual_payload = client.make_request(
        method_name,
        naver,
        {
            'Content-type': 'application/json;charset=utf-8',
            'Accepts': 'application/json'
        },
        payload
    )
    assert actual_method == method_name
    assert request_url == naver
    assert payload == json.loads(actual_payload.decode('utf-8'))
    assert header == {'Content-type': 'application/json;charset=utf-8',
                      'Accepts': 'application/json'}
    with raises(ValueError):
        request_url, header, actual_payload = client.make_request(
            u'FOO',
            naver,
            {
                'Content-type': 'application/json;charset=utf-8',
                'Accepts': 'application/json'
            },
            payload
        )


def test_client_ping():
    url = u'http://foobar.com/rpc/'
    client = Client(url, MockOpener(url, MusicServiceImpl))
    assert client.ping()


@mark.parametrize(
    'url',
    [u'http://foobar.com/rpc/', 'http://foobar.com/rpc/']
)
def test_client_url(url):
    client = Client(url, MockOpener(url, MusicServiceImpl))
    assert client.ping()


@mark.parametrize('method', [u'POST', 'POST'])
def test_client_make_request_method_type(method):
    url = 'http://test.com'
    client = MethodClient(method, url,
                          MockOpener(url, MusicServiceImpl))
    assert client.ping()


@mark.parametrize('arity', [0, 1, 2, 3, 5])
def test_client_make_request_arity_check(arity):
    class ExtendedClient(Client):
        def make_request(self, method, request_url, headers, payload):
            return (method, request_url, headers,
                    json.dumps(payload).encode('utf-8'), None)[:arity]
    url = 'http://foobar.com/rpc/'
    client = ExtendedClient(url, MockOpener(url, MusicServiceImpl))
    with raises(TypeError) as e:
        client.remote_call('ping', {})
    assert str(e.value).startswith(
        'make_request() must return a triple of '
        '(method, request_url, headers, content), not '
    )


def test_rpc_error_types():
    url = u'http://foobar.com/rpc/'
    client = nf.MusicService_Client(url, MockOpener(url, MusicServiceImpl))
    with raises(nf.Unknown):
        client.get_music_by_artist_name('error')
    with raises(nf.BadRequest):
        client.get_music_by_artist_name('adele')
