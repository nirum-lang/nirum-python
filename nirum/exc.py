""":mod:nirum.exc`
~~~~~~~~~~~~~~~~~~

"""
__all__ = (
    'InvalidNirumServiceMethodNameError',
    'InvalidNirumServiceMethodTypeError',
    'NirumProcedureArgumentError',
    'NirumProcedureArgumentRequiredError',
    'NirumProcedureArgumentValueError',
    'NirumServiceError',
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


class UnexpectedNirumResponseError(IOError):
    """TODO"""
