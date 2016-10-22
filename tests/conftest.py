from pytest import fixture

from .nirum_schema import import_nirum_fixture


nirum_fixture = import_nirum_fixture()


@fixture
def fx_unboxed_type():
    return nirum_fixture.Offset


@fixture
def fx_offset(fx_unboxed_type):
    return fx_unboxed_type(1.2)


@fixture
def fx_record_type():
    return nirum_fixture.Point


@fixture
def fx_point(fx_record_type, fx_unboxed_type):
    return fx_record_type(fx_unboxed_type(3.14), fx_unboxed_type(1.592))


@fixture
def fx_circle_type():
    return nirum_fixture.Circle


@fixture
def fx_rectangle_type():
    return nirum_fixture.Rectangle


@fixture
def fx_rectangle(fx_rectangle_type, fx_point):
    return fx_rectangle_type(fx_point, fx_point)


@fixture
def fx_layered_boxed_types():
    return nirum_fixture.A, nirum_fixture.B, nirum_fixture.C


@fixture
def fx_location_record():
    return nirum_fixture.Location


@fixture
def fx_shape_type():
    return nirum_fixture.Shape


@fixture
def fx_token_type():
    return nirum_fixture.Token
