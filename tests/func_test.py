import collections

from pytest import raises

from nirum.func import import_string


def test_import_string():
    assert import_string('collections:OrderedDict') == collections.OrderedDict
    assert import_string('collections:OrderedDict({"a": 1})') == \
            collections.OrderedDict({"a": 1})
    with raises(ValueError):
        # malformed
        import_string('world')
    with raises(NameError):
        # coudn't import
        import_string('os:world')
    with raises(ImportError):
        # coudn't import
        import_string('os.hello:world')
