from pytest import raises

from nirum.validate import validate_boxed_type


def test_validate_boxed_type(fx_offset, fx_boxed_type):
    assert validate_boxed_type(fx_offset, float)
    wrong_boxed_type = fx_boxed_type('hello')
    with raises(TypeError):
        validate_boxed_type(wrong_boxed_type, float)
