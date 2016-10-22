import decimal

from pytest import raises
from six import text_type

from nirum.validate import (validate_unboxed_type, validate_record_type,
                            validate_union_type)


def test_validate_unboxed_type():
    assert validate_unboxed_type(3.14, float)
    with raises(TypeError):
        validate_unboxed_type(u'hello', float)


def test_validate_record_type(fx_point, fx_record_type, fx_offset,
                              fx_location_record):
    assert validate_record_type(fx_point)
    with raises(TypeError):
        validate_record_type(fx_record_type(left=fx_offset, top=1))
    with raises(TypeError):
        validate_record_type(fx_record_type(left=1, top=fx_offset))
    assert validate_record_type(
        fx_location_record(name=None, lat=decimal.Decimal('3.14'),
                           lng=decimal.Decimal('1.592'))
    )


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
    assert validate_unboxed_type(u'test', text_type)
    assert validate_unboxed_type(A(u'test'), A)
    assert validate_unboxed_type(B(A(u'test')), B)
    with raises(TypeError):
        assert validate_unboxed_type(u'test', A)

    with raises(TypeError):
        assert validate_unboxed_type(u'test', B)

    with raises(TypeError):
        assert validate_unboxed_type(A(u'test'), B)
