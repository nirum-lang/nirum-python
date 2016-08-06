import json
import typing

from pytest import fixture, raises, mark
from werkzeug.test import Client
from werkzeug.wrappers import Response

from nirum.constructs import NameDict
from nirum.exc import (InvalidNirumServiceMethodTypeError,
                       InvalidNirumServiceMethodNameError)
from nirum.rpc import Service, WsgiApp


class MusicService(Service):

    __nirum_service_methods__ = {
        'get_music_by_artist_name': {
            'artist_name': str,
            '_return': typing.Sequence[str],
            '_names': NameDict([
                ('artist_name', 'artist_name')
            ])
        },
        'incorrect_return': {
            '_return': str,
            '_names': NameDict([])
        },
        'get_artist_by_music': {
            'music': str,
            '_return': str,
            '_names': NameDict([('music', 'norae')])
        }
    }
    __nirum_method_names__ = NameDict([
        ('get_music_by_artist_name', 'get_music_by_artist_name'),
        ('incorrect_return', 'incorrect_return'),
        ('get_artist_by_music', 'find_artist'),
    ])

    def get_music_by_artist_name(
        self,
        artist_name: str
    ) -> typing.Sequence[str]:
        raise NotImplementedError('get_music_by_artist_name')

    def incorrect_return(self) -> str:
        raise NotImplementedError('incorrect_return')

    def get_artist_by_music(self, music: str) -> str:
        raise NotImplementedError('get_artist_by_music')


class MusicServiceImpl(MusicService):

    music_map = {
        'damien rice': ['9 crimes', 'Elephant'],
        'ed sheeran': ['Thinking out loud', 'Photograph'],
    }

    def get_music_by_artist_name(
        self,
        artist_name: str
    ) -> typing.Sequence[str]:
        return self.music_map.get(artist_name)

    def incorrect_return(self) -> str:
        return 1

    def get_artist_by_music(self, music: str) -> str:
        for k, v in self.music_map.items():
            if music in v:
                return k
        return 'none'


class MusicServiceNameErrorImpl(MusicService):

    __nirum_service_methods__ = {
        'foo': {}
    }


class MusicServiceTypeErrorImpl(MusicService):

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
    return Client(fx_music_wsgi, Response)


def test_wsgi_app_ping(fx_music_wsgi, fx_test_client):
    assert fx_music_wsgi.service
    response = fx_test_client.get('/ping/')
    data = json.loads(response.get_data(as_text=True))
    assert 'Ok' == data


def assert_response(response, status_code, expect_json):
    assert response.status_code == status_code
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
                       "expected 'str'."
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
                       "expected 'str'."
        }
    )


@mark.parametrize(
    'payload, expected_json',
    [
        ({'artist_name': 'damien rice'}, ['9 crimes', 'Elephant']),
        ({'artist_name': 'ed sheeran'}, ['Thinking out loud', 'Photograph']),
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
    payload = {'norae': '9 crimes'}
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
        'damien rice'
    )
