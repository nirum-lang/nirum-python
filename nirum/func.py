import re

from six.moves import urllib, reduce

__all__ = 'IMPORT_RE', 'import_string', 'url_endswith_slash'
IMPORT_RE = re.compile(
    r'''^
        (?P<modname> (?!\d) [\w]+
                     (?: \. (?!\d)[\w]+ )*
        )
        :
        (?P<clsexp> (?P<clsname> (?!\d) \w+ )
                    (?: \(.*\) )?
        )
    $''',
    re.X
)


def url_endswith_slash(url):
    scheme, netloc, path, _, _ = urllib.parse.urlsplit(url)
    if not (scheme and netloc):
        raise ValueError("{} isn't URL.".format(url))
    if not path.endswith('/'):
        path += '/'
    return urllib.parse.urlunsplit((scheme, netloc, path, '', ''))


def import_string(imp):
    m = IMPORT_RE.match(imp)
    if not m:
        raise ValueError(
            "malformed expression: {}, have to be x.y:z(...)".format(imp)
        )
    module_name = m.group('modname')
    import_root_mod = __import__(module_name)
    # it is used in `eval()`
    import_mod = reduce(getattr, module_name.split('.')[1:], import_root_mod) # noqa
    class_expression = m.group('clsexp')
    try:
        v = eval(class_expression, import_mod.__dict__, {})
    except AttributeError:
        raise ValueError("Can't import {}".format(imp))
    else:
        return v
