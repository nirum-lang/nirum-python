from pytest import raises

from nirum.constructs import NameDict


def test_name_dict():
    nd = NameDict([('left', 'x'), ('right', 'right')])
    assert nd['left'] == 'x'
    assert nd['right'] == 'right'
    assert nd.behind_names['right'] == 'right'
    assert len(nd) == 2
    assert set(list(nd)) == set(['left', 'right'])
    with raises(KeyError):
        nd['top']
    with raises(KeyError):
        nd.behind_names['left']


def test_name_dict_assert():
    with raises(AssertionError):
        NameDict([('left', 'x'), ('right', 'x')])
    with raises(AssertionError):
        NameDict([('left', 'x'), ('left', 'y')])
