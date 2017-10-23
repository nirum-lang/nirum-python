from fixture import (A, B, C, Circle, Location, Offset, Point,
                     Rectangle, Shape, Token)
from pytest import fixture


@fixture
def fx_unboxed_type():
    return Offset


@fixture
def fx_offset(fx_unboxed_type):
    return fx_unboxed_type(1.2)


@fixture
def fx_record_type():
    return Point


@fixture
def fx_point(fx_record_type, fx_unboxed_type):
    return fx_record_type(left=fx_unboxed_type(3.14),
                          top=fx_unboxed_type(1.592))


@fixture
def fx_circle_type():
    return Circle


@fixture
def fx_rectangle_type():
    return Rectangle


@fixture
def fx_rectangle(fx_rectangle_type, fx_point):
    return fx_rectangle_type(upper_left=fx_point, lower_right=fx_point)


@fixture
def fx_layered_boxed_types():
    return A, B, C


@fixture
def fx_location_record():
    return Location


@fixture
def fx_shape_type():
    return Shape


@fixture
def fx_token_type():
    return Token
