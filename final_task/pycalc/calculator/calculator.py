"""
Initialization of a calculator. Return a calculator instance.
"""

from pycalc.lexer import Lexer
from pycalc.parser import Parser, ParserGenericError
from pycalc.importer import ModuleImportErrors

from .formatters import err_msg_with_ctx_formatter, err_modules_import_formatter
from .errors import CalculatorCalculationError, CalculatorInitializationError, get_err_msg
from .importer import build_modules_registry
from .matchers import build_matchers
from .messages import (
    CALCULATOR_INITIALIZATION_ERROR,
    CANT_PARSE_EXPRESSION,
    EMPTY_EXPRESSION_PROVIDED,
)
from .precedence import Precedence
from .specification import build_specification


class Calculator:
    """
    The calculator class.

    Provide a method to calculate an expression from a string.
    """

    def __init__(self, parser):
        self._parser = parser

    def calculate(self, expression):
        """
        Calculate an expression.

        Return result of calculation or raise a `CalculatorCalculationError` exception
        if calculation fails.
        """

        # empty expression
        if not expression:
            raise CalculatorCalculationError(EMPTY_EXPRESSION_PROVIDED)

        # calculate an expression
        try:
            result = self._parser.parse(expression)
            return result

        # handle calculation errors
        except ParserGenericError as exc_wrapper:

            # ’unwrap’ an original exception and get context
            exc = exc_wrapper.__cause__
            ctx = exc.ctx if hasattr(exc, 'ctx') else exc_wrapper.ctx

            # an error message
            err_msg = get_err_msg(exc)
            err_msg = err_msg_with_ctx_formatter(err_msg, ctx)

        # handle all other errors
        except Exception as exc:
            err_msg = CANT_PARSE_EXPRESSION

        raise CalculatorCalculationError(err_msg)


def calculator(modules_names=None):
    """
    Initialize a calculator and return a Calculator instance.

    Raise a `CalculatorInitializationError` exception when initialization fails."""

    try:
        # import constants and functions from default and requested modules
        modules_registry = build_modules_registry(modules_names)

        # build lexemes matchers
        matchers = build_matchers(modules_registry)

        # create a lexer
        lexer = Lexer(matchers)

        # build a specification for a parser
        spec = build_specification(modules_registry)

        # create a parser
        power = Precedence.DEFAULT
        parser = Parser(spec, lexer, power)

        # create a calculator
        calculator_ = Calculator(parser)

        return calculator_

    except ModuleImportErrors as exc:
        modules_names = exc.modules_names
        err_msg = err_modules_import_formatter(modules_names)

    except Exception:
        err_msg = CALCULATOR_INITIALIZATION_ERROR

    raise CalculatorInitializationError(err_msg)
