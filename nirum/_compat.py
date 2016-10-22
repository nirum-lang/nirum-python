import datetime

__all__ = 'utc',


try:
    utc = datetime.timezone.utc
except AttributeError:
    ZERO = datetime.timedelta(0)
    HOUR = datetime.timedelta(hours=1)

    class UTC(datetime.tzinfo):
        """UTC"""

        def utcoffset(self, dt):
            return ZERO

        def tzname(self, dt):
            return "UTC"

        def dst(self, dt):
            return ZERO

    utc = UTC()
