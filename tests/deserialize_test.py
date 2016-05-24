from pytest import raises

from nirum.serialize import serialize_record_type
from nirum.deserialize import (deserialize_boxed_type, deserialize_meta,
                               deserialize_record_type, deserialize_union_type)


def test_deserialize_boxed_type(fx_boxed_type):
    v = 3.14
    assert fx_boxed_type(v) == deserialize_boxed_type(fx_boxed_type, v)


def test_deserialize_record_type(fx_boxed_type, fx_record_type):
    with raises(ValueError):
        deserialize_record_type(fx_record_type, {})

    with raises(ValueError):
        deserialize_record_type(fx_record_type, {'_type': 'hello'})

    left = fx_boxed_type(1.1)
    top = fx_boxed_type(2.2)
    deserialized = deserialize_record_type(
        fx_record_type, {'_type': 'point', 'x': left.value, 'top': top.value}
    )
    instance = fx_record_type(left=left, top=top)
    assert deserialized == instance


def test_deserialize_union_type(fx_circle_type, fx_rectangle_type,
                                fx_point):
    with raises(ValueError):
        deserialize_union_type(fx_circle_type, {})

    with raises(ValueError):
        deserialize_union_type(fx_circle_type, {'_type': 'shape'})

    with raises(ValueError):
        deserialize_union_type(fx_circle_type,
                               {'_type': 'foo', '_tag': 'circle'})
    with raises(ValueError):
        deserialize_union_type(fx_rectangle_type,
                               {'_type': 'shape', '_tag': 'circle'})

    deserialize = deserialize_union_type(
        fx_rectangle_type,
        {
            '_type': 'shape', '_tag': 'rectangle',
            'upper_left': serialize_record_type(fx_point),
            'lower_right': serialize_record_type(fx_point),
        }
    )
    assert deserialize.upper_left == fx_point
    assert deserialize.lower_right == fx_point


def test_deserialize_meta_error():
    with raises(TypeError):
        deserialize_meta(None, {})


def test_deserialize_meta_record(fx_boxed_type, fx_record_type, fx_point):
    left = fx_boxed_type(1.1)
    top = fx_boxed_type(2.2)
    d = {'_type': 'point', 'x': left.value, 'top': top.value}
    meta = deserialize_meta(fx_record_type, d)
    record = deserialize_record_type(fx_record_type, d)
    assert meta == record


def test_deserialize_meta_union(fx_rectangle_type, fx_point):
    d = {
        '_type': 'shape', '_tag': 'rectangle',
        'upper_left': serialize_record_type(fx_point),
        'lower_right': serialize_record_type(fx_point),
    }
    meta = deserialize_meta(fx_rectangle_type, d)
    union = deserialize_union_type(
        fx_rectangle_type, d
    )
    assert meta == union


def test_deserialize_meta_boxed(fx_boxed_type, fx_record_type, fx_point):
    v = 3.14
    meta = deserialize_meta(fx_boxed_type, v)
    boxed = fx_boxed_type(v)
    assert meta == boxed
