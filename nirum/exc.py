""":mod:nirum.exc`
~~~~~~~~~~~~~~~~~~

"""
import urllib.error

__all__ = (
    'InvalidNirumServiceMethodNameError',
    'InvalidNirumServiceMethodTypeError',
    'NirumHttpError',
    'NirumProcedureArgumentError',
    'NirumProcedureArgumentRequiredError',
    'NirumProcedureArgumentValueError',
    'NirumServiceError',
    'NirumUrlError',
    'UnexpectedNirumResponseError',
)


class NirumServiceError(Exception):
    """Base nirum service error"""


class InvalidNirumServiceMethodNameError(ValueError, NirumServiceError):
    """Raised when nirum service has invalid method name."""


class InvalidNirumServiceMethodTypeError(TypeError, NirumServiceError):
    """Raised when nirum service method is not callable."""


class NirumProcedureArgumentError(ValueError, NirumServiceError):
    """WIP"""


class NirumProcedureArgumentRequiredError(NirumProcedureArgumentError):
    """WIP"""


class NirumProcedureArgumentValueError(NirumProcedureArgumentError):
    """WIP"""


class NirumHttpError(urllib.error.HTTPError, NirumServiceError):
    """TODO"""


class NirumUrlError(urllib.error.URLError, NirumServiceError):
    """TODO"""

    def __init__(self, exc: urllib.error.URLError):
        self.text = exc.read()
        super().__init__(exc.reason)


class UnexpectedNirumResponseError(NirumHttpError):
    """TODO"""
