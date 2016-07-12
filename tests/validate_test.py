from pytest import raises

from nirum.validate import (validate_boxed_type, validate_record_type,
                            validate_union_type)


def test_validate_boxed_type():
    assert validate_boxed_type(3.14, float)
    with raises(TypeError):
        validate_boxed_type('hello', float)


def test_validate_record_type(fx_point, fx_record_type, fx_offset):
    assert validate_record_type(fx_point)
    with raises(TypeError):
        validate_record_type(fx_record_type(left=fx_offset, top=1))
    with raises(TypeError):
        validate_record_type(fx_record_type(left=1, top=fx_offset))


def test_validate_union_type(fx_rectangle, fx_rectangle_type, fx_point):
    assert validate_union_type(fx_rectangle)
    with raises(TypeError):
        validate_union_type(fx_rectangle_type(1, fx_point))

    with raises(TypeError):
        validate_union_type(fx_rectangle_type(fx_point, 1))

    with raises(TypeError):
        validate_union_type(fx_rectangle_type(1, 1))


def test_validate_layered_boxed_types(fx_layered_boxed_types):
    A, B, C = fx_layered_boxed_types
    assert validate_boxed_type('test', str)
    assert validate_boxed_type(A('test'), A)
    assert validate_boxed_type(B(A('test')), B)
    with raises(TypeError):
        assert validate_boxed_type('test', A)

    with raises(TypeError):
        assert validate_boxed_type('test', B)

    with raises(TypeError):
        assert validate_boxed_type(A('test'), B)
