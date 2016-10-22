import datetime
import decimal
import uuid
import typing

from pytest import raises, mark
from six import text_type

from nirum._compat import utc
from nirum.serialize import serialize_record_type
from nirum.deserialize import (deserialize_unboxed_type, deserialize_meta,
                               deserialize_tuple_type,
                               deserialize_record_type, deserialize_union_type,
                               deserialize_optional, deserialize_primitive)


def test_deserialize_unboxed_type(fx_unboxed_type, fx_token_type):
    v = 3.14
    assert fx_unboxed_type(v) == deserialize_unboxed_type(fx_unboxed_type, v)
    uuid_ = uuid.uuid4()
    t = str(uuid_)
    assert fx_token_type(uuid_) == deserialize_unboxed_type(fx_token_type, t)


def test_deserialize_record_type(fx_unboxed_type, fx_record_type):
    with raises(ValueError):
        deserialize_record_type(fx_record_type, {})

    with raises(ValueError):
        deserialize_record_type(fx_record_type, {'_type': 'hello'})

    left = fx_unboxed_type(1.1)
    top = fx_unboxed_type(2.2)
    deserialized = deserialize_record_type(
        fx_record_type, {'_type': 'point', 'x': left.value, 'top': top.value}
    )
    instance = fx_record_type(left=left, top=top)
    assert deserialized == instance


def test_deserialize_union_type(fx_circle_type, fx_rectangle_type,
                                fx_point, fx_shape_type):
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

    with raises(ValueError):
        deserialize_union_type(fx_shape_type,
                               {'_type': 'shape', '_tag': 'semo'})

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


def test_deserialize_meta_record(fx_unboxed_type, fx_record_type, fx_point):
    left = fx_unboxed_type(1.1)
    top = fx_unboxed_type(2.2)
    d = {'_type': 'point', 'x': left.value, 'top': top.value}
    meta = deserialize_meta(fx_record_type, d)
    record = deserialize_record_type(fx_record_type, d)
    assert meta == record


def test_deserialize_meta_union(fx_rectangle_type, fx_point, fx_shape_type):
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
    meta_from_shape = deserialize_meta(fx_shape_type, d)
    assert meta_from_shape == meta


def test_deserialize_meta_unboxed(fx_unboxed_type, fx_record_type, fx_point,
                                  fx_token_type):
    v = 3.14
    meta = deserialize_meta(fx_unboxed_type, v)
    unboxed = fx_unboxed_type(v)
    assert meta == unboxed
    v = uuid.uuid4()
    meta = deserialize_meta(fx_token_type, str(v))
    unboxed = fx_token_type(v)
    assert meta == unboxed


def test_deserialize_multiple_boxed_type(fx_layered_boxed_types):
    A, B, C = fx_layered_boxed_types
    assert B.__nirum_deserialize__(u'lorem') == B(A(u'lorem'))
    assert C.__nirum_deserialize__(u'x') == C(B(A(u'x')))
    with raises(ValueError):
        B.__nirum_deserialize__(1)


@mark.parametrize(
    'data, t, expect',
    [
        (1, int, 1),
        (1.1, float, 1.1),
        (u'hello', text_type, 'hello'),
        (True, bool, True),
        ('1.1', decimal.Decimal, decimal.Decimal('1.1')),
        (
            '2016-08-04T01:42:43Z',
            datetime.datetime,
            datetime.datetime(
                2016, 8, 4, 1, 42, 43, tzinfo=utc
            )
        ),
        (
            '2016-08-04',
            datetime.date,
            datetime.date(2016, 8, 4)
        ),
        (
            'E41E8A85-2E99-4493-8192-0D3AA3D8D005',
            uuid.UUID,
            uuid.UUID('E41E8A85-2E99-4493-8192-0D3AA3D8D005'),
        )
    ]
)
def test_deserialize_primitive(data, t, expect):
    assert deserialize_primitive(t, data) == expect


@mark.parametrize(
    'data, t',
    [
        ('a', int),
        ('a', float),
        ('a', decimal.Decimal),
        ('a', datetime.datetime),
        ('a', datetime.date),
        ('a', uuid.UUID),
        (1, text_type),
        (1.1, text_type),
    ]
)
def test_deserialize_primitive_error(data, t):
    with raises(ValueError):
        deserialize_primitive(t, data)


@mark.parametrize(
    'primitive_type, iter_, expect_iter',
    [
        (text_type, [u'a', u'b'], None),
        (float, [3.14, 1.592], None),
        (
            decimal.Decimal,
            ['3.14', '1.59'],
            [decimal.Decimal('3.14'), decimal.Decimal('1.59')]
        ),
        (
            uuid.UUID,
            [
                '862c4c1d-ece5-4d04-aa1f-485797244e14',
                'e05b4319-fca1-4637-992b-344e45be7ff9'
            ],
            [
                uuid.UUID('862c4c1d-ece5-4d04-aa1f-485797244e14'),
                uuid.UUID('e05b4319-fca1-4637-992b-344e45be7ff9')
            ],
        ),
        (
            datetime.datetime,
            [
                '2016-08-04T01:29:16Z',
                '20160804T012916Z',
            ],
            [
                datetime.datetime(
                    2016, 8, 4, 1, 29, 16,
                    tzinfo=utc
                ),
                datetime.datetime(
                    2016, 8, 4, 1, 29, 16,
                    tzinfo=utc
                ),
            ],
        ),
        (
            datetime.date,
            [
                '2016-08-04',
                '2016-08-05'
            ],
            [
                datetime.date(2016, 8, 4),
                datetime.date(2016, 8, 5)
            ],
        ),
        (bool, [True, False], None),
    ]
)
@mark.parametrize(
    'abstract_type, python_type',
    [
        (typing.Sequence, list),
        (typing.List, list),
        (typing.Set, set),
        (typing.AbstractSet, set),
    ]
)
def test_deserialize_meta_iterable(
    primitive_type, iter_, abstract_type, python_type, expect_iter
):
    deserialized = deserialize_meta(abstract_type[primitive_type], iter_)
    if expect_iter is None:
        expect_iter = iter_
    assert deserialized == python_type(expect_iter)


def test_deserialize_tuple():
    assert deserialize_tuple_type(typing.Tuple, (1, 2)) == (1, 2)
    assert deserialize_tuple_type(
        typing.Tuple[text_type, int], (u'a', 1)
    ) == (u'a', 1)
    with raises(ValueError):
        deserialize_tuple_type(typing.Tuple[text_type], (u'a', 1))

    with raises(ValueError):
        deserialize_tuple_type(typing.Tuple[text_type, text_type], (u'a'))

    with raises(ValueError):
        deserialize_tuple_type(typing.Tuple[text_type, text_type], (u'a', 1))


def test_deserialize_optional(fx_record_type):
    assert deserialize_optional(typing.Optional[text_type], u'abc') == u'abc'
    assert deserialize_optional(typing.Optional[text_type], None) is None
    assert deserialize_optional(typing.Optional[fx_record_type], None) is None
    with raises(ValueError):
        deserialize_optional(typing.Union[text_type, int], u'text_type')
    with raises(ValueError):
        deserialize_optional(typing.Union[text_type, int], 1)
    with raises(ValueError):
        deserialize_optional(typing.Union[text_type, int], None)
    with raises(ValueError):
        deserialize_optional(typing.Optional[text_type], 1)
