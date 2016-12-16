import json

from pytest import fixture, raises, mark
from six import text_type
from werkzeug.test import Client as TestClient
from werkzeug.wrappers import Response

from nirum.exc import (InvalidNirumServiceMethodTypeError,
                       InvalidNirumServiceMethodNameError)
from nirum.rpc import Client, WsgiApp
from nirum.test import MockOpener

from .nirum_schema import import_nirum_fixture


nf = import_nirum_fixture()


class MusicServiceImpl(nf.MusicService):

    music_map = {
        u'damien rice': [u'9 crimes', u'Elephant'],
        u'ed sheeran': [u'Thinking out loud', u'Photograph'],
    }

    def get_music_by_artist_name(self, artist_name):
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
        'foo': {}
    }


class MusicServiceTypeErrorImpl(nf.MusicService):

    get_music_by_artist_name = 1


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


def test_rpc_internal_error(fx_test_client):
    response = fx_test_client.post('/?method=raise_application_error_request')
    assert response.status_code == 500, response.get_data(as_text=True)
    actual_response_json = json.loads(
        response.get_data(as_text=True)
    )
    expected_json = {
        '_type': 'error',
        '_tag': 'internal_server_error',
        'message': 'hello world'
    }
    assert actual_response_json == expected_json


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


def test_rpc_client_service(monkeypatch):
    url = u'http://foobar.com/'
    client = nf.MusicServiceClient(url, MockOpener(url, MusicServiceImpl))
    nine_crimes = '9 crimes'
    damien_music = [nine_crimes, 'Elephant']
    damien_rice = 'damien rice'
    assert client.get_music_by_artist_name(damien_rice) == damien_music
    assert client.get_artist_by_music(nine_crimes) == damien_rice


@mark.parametrize('method_name', ['POST', 'post'])
def test_rpc_client_make_request(method_name, monkeypatch):
    naver = u'http://naver.com'
    payload = {'hello': 'world'}
    client = nf.MusicServiceClient(naver, MockOpener(naver, MusicServiceImpl))
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
