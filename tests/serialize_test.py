import typing

from pytest import raises

from nirum.serialize import serialize_boxed_type


def test_serialize_boxed_type(fx_offset):
    assert serialize_boxed_type(fx_offset) == fx_offset.value
