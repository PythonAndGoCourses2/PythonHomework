"""
Provides functions to compose an error message
according to an exception type.
"""

from pycalc.parser import errors as parser_err
from pycalc.specification import errors as spec_err
from .parselets import errors as parselet_err

from .messages import SYNTAX_ERROR, CANT_PARSE_EXPRESSION

SYNTAX_ERROR_EXCEPIONS = (
    parser_err.ParserNoTokenReceived,
    parser_err.ParserExpectedTokenAbsent,
    parser_err.ParserSourceNotExhausted,
    spec_err.NudDenotationError,
    spec_err.LedDenotationError
)


class CalculatorError(Exception):
    """Raise on calculator’s errors."""

    def __init__(self, err_msg):
        super().__init__()
        self.err_msg = err_msg


class CalculatorInitializationError(CalculatorError):
    """Raise on calculator’s initialization errors."""


class CalculatorCalculationError(CalculatorError):
    """Raise on calculator’s calculation errors."""


def get_err_msg(exc):
    """Return an error message according to an exception type."""

    # for function calls and operator applying errors
    if isinstance(exc, parselet_err.CallError):
        # get the error message of the original exception
        err_msg = str(exc.__cause__)

    # for exceptions that mean a syntax error
    elif isinstance(exc, SYNTAX_ERROR_EXCEPIONS):
        err_msg = SYNTAX_ERROR

    # for all others exception
    else:
        err_msg = CANT_PARSE_EXPRESSION

    return err_msg
