from pytest import raises

from nirum.validate import validate_boxed_type, validate_record_type


def test_validate_boxed_type():
    assert validate_boxed_type(3.14, float)
    with raises(TypeError):
        validate_boxed_type('hello', float)


def test_validate_record_type(fx_point, fx_record_type, fx_offset):
    assert validate_record_type(fx_point)
    with raises(TypeError):
        assert validate_record_type(fx_record_type(left=fx_offset, top=1))
    with raises(TypeError):
        assert validate_record_type(fx_record_type(left=1, top=fx_offset))
