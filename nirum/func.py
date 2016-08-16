import urllib.parse

__all__ = 'url_endswith_slash',


def url_endswith_slash(url: str) -> str:
    scheme, netloc, path, _, _ = urllib.parse.urlsplit(url)
    if not (scheme and netloc):
        raise ValueError("{} isn't URL.".format(url))
    if not path.endswith('/'):
        path += '/'
    return urllib.parse.urlunsplit((scheme, netloc, path, '', ''))
