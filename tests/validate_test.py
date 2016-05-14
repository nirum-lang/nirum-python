from pytest import raises

from nirum.validate import validate_boxed_type


def test_validate_boxed_type():
    assert validate_boxed_type(3.14, float)
    with raises(TypeError):
        validate_boxed_type('hello', float)
