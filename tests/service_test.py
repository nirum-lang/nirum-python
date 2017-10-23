from fixture import MusicService
from pytest import mark, raises

from nirum.exc import (InvalidNirumServiceMethodNameError,
                       InvalidNirumServiceMethodTypeError)


class MusicServiceNameErrorImpl(MusicService):

    __nirum_service_methods__ = {
        'foo': {'_v': 2}
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
