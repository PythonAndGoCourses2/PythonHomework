"""
Initialization of a calculator. Return a calculator instance.
"""

from pycalc.lexer import Lexer
from pycalc.parser import Parser, ParserGenericError

from .formatters import err_msg_formatter, err_ctx_formatter
from .errors import get_err_msg
from .importer import build_modules_registry
from .matchers import build_matchers
from .messages import (
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

        Return result of a calculation or an error message
        if the calculation fails.
        """

        # empty expression
        if not expression:
            return err_msg_formatter(EMPTY_EXPRESSION_PROVIDED)

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
            err_msg = err_msg_formatter(err_msg)

            # an context message
            ctx_msg = err_ctx_formatter(ctx)

            return f'{err_msg}\n{ctx_msg}'

        # probably not reacheable code but better save than sorry
        except Exception as exc:

            err_msg = err_msg_formatter(CANT_PARSE_EXPRESSION)

            return err_msg


def calculator(modules_names=None):
    """Initialize a calculator and return a parser object."""

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
