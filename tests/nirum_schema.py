from six import PY2, PY3


def import_nirum_fixture():
    if PY2:
        nirum_fixture_name = 'tests.py2_nirum'
    elif PY3:
        nirum_fixture_name = 'tests.py3_nirum'
    else:
        raise ImportError()
    return __import__(
        nirum_fixture_name,
        globals(),
        locals(),
        [
            'A', 'B', 'C', 'Circle', 'Location', 'MusicService',
            'MusicServiceClient', 'Offset', 'Point', 'Rectangle', 'Shape',
            'Token',
        ]
    )
