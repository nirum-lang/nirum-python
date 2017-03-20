import collections
import pickle

from pytest import raises

from nirum.datastructures import List, Map


def test_map_init():
    assert list(Map()) == []
    assert (sorted(Map([('a', 1), ('b', 2)]).items()) ==
            sorted(Map({'a': 1, 'b': 2}).items()) ==
            sorted(Map(Map({'a': 1, 'b': 2})).items()) ==
            sorted(Map(a=1, b=2).items()) ==
            sorted(Map([('a', 1)], b=2).items()) ==
            sorted(Map({'a': 1}, b=2).items()) ==
            sorted(Map(Map([('a', 1)]), b=2).items()) ==
            [('a', 1), ('b', 2)])
    assert isinstance(Map(), collections.Mapping)
    assert not isinstance(Map(), collections.MutableMapping)


def test_map_iter():
    assert list(Map()) == []
    assert list(Map(a=1)) == ['a']
    assert list(Map(a=1, b=2)) in (['a', 'b'], ['b', 'a'])


def test_map_len():
    assert len(Map()) == 0
    assert len(Map(a=1)) == 1
    assert len(Map(a=1, b=2)) == 2


def test_map_getitem():
    m = Map(a=1, b=2)
    assert m['a'] == m.get('a') == m.get('a', 0) == 1
    assert m['b'] == m.get('b') == m.get('b', 0) == 2
    with raises(KeyError):
        m['c']
    assert m.get('c') is None
    assert m.get('c', 0) == 0


def test_map_contains():
    m = Map(a=1, b=2)
    assert 'a' in m
    assert 'b' in m
    assert 'c' not in m


def test_map_pickle():
    def p(v):
        assert pickle.loads(pickle.dumps(v)) == v
    p(Map())
    p(Map(a=1))
    p(Map(a=1, b=2))
    p(Map(d=Map(a=1, b=2)))


def test_map_bool():
    assert not Map()
    assert Map(a=1)
    assert Map(a=1, b=2)


def test_map_repr():
    assert repr(Map()) == 'nirum.datastructures.Map()'
    assert repr(Map(a=1)) == "nirum.datastructures.Map({'a': 1})"
    assert repr(Map(a=1, b=2)) == "nirum.datastructures.Map({'a': 1, 'b': 2})"


def test_list():
    immutable_list = List([1, 2])
    with raises(AttributeError):
        immutable_list.append(1)

    with raises(TypeError):
        immutable_list + [3]

    assert isinstance(immutable_list, collections.Sequence)
    assert not isinstance(immutable_list, collections.MutableSequence)
    assert immutable_list[0] == 1
    assert len(immutable_list) == 2
    assert 2 in immutable_list
    assert next(iter(immutable_list)) == 1
    assert immutable_list.index(2) == 1
    assert immutable_list.count(1) == 1
    assert immutable_list.count(2) == 1
    assert immutable_list.count(3) == 0
