from nirum.serialize import (serialize_boxed_type, serialize_record_type,
                             serialize_union_type)


def test_serialize_boxed_type(fx_offset):
    assert serialize_boxed_type(fx_offset) == fx_offset.value


def test_serialize_layered_boxed_type(fx_layered_boxed_types):
    actual = fx_layered_boxed_types[1](fx_layered_boxed_types[0]('test'))
    assert actual.__nirum_serialize__() == 'test'


def test_serialize_record_type(fx_point):
    assert serialize_record_type(fx_point) == {'_type': 'point', 'x': 3.14,
                                               'top': 1.592}


def test_serialize_union_type(fx_point, fx_offset, fx_circle_type,
                              fx_rectangle_type):
    circle = fx_circle_type(fx_point, fx_offset)
    s = {
        '_type': 'shape', '_tag': 'circle',
        'origin': serialize_record_type(fx_point),
        'radius': serialize_boxed_type(fx_offset)
    }
    assert serialize_union_type(circle) == s
    rectangle = fx_rectangle_type(fx_point, fx_point)
    s = {
        '_type': 'shape', '_tag': 'rectangle',
        'upper_left': serialize_record_type(fx_point),
        'lower_right': serialize_record_type(fx_point),
    }
    assert serialize_union_type(rectangle) == s


def test_multiple_boxed_type(fx_layered_boxed_types):
    A, B, _ = fx_layered_boxed_types
    assert B(A('hello')).value.value == 'hello'
    assert B(A('lorem')).__nirum_serialize__() == 'lorem'
