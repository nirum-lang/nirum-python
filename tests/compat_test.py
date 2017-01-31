import itertools
import typing

from pytest import mark
from six import text_type
from nirum._compat import (get_abstract_param_types,
                           get_tuple_param_types,
                           get_union_types,
                           is_union_type)

primitives = [text_type, int, float, bytes]


@mark.parametrize('type_', primitives)
@mark.parametrize('abstract_type', [typing.AbstractSet, typing.Sequence])
def test_get_abstract_param_types(abstract_type, type_):
    actual_types = get_abstract_param_types(abstract_type[type_])
    assert actual_types == (type_, )


@mark.parametrize('types', itertools.product(primitives, repeat=2))
def test_get_tuple_param_types(types):
    assert get_tuple_param_types(typing.Tuple[types[0], types[1]]) == types


@mark.parametrize('types', itertools.permutations(primitives, 2))
def test_get_union_types(types):
    assert get_union_types(typing.Union[types[0], types[1]]) == types


@mark.parametrize('types', itertools.permutations(primitives, 2))
def test_is_union_type(types):
    assert is_union_type(typing.Union[types[0], types[1]])
