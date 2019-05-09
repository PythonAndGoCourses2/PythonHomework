"""
Initialization of a calculator. Returns a calculator instance.
"""

from pycalc.lexer import Lexer
from pycalc.parser import Parser, ParserGenericError
from pycalc.token.precedence import Precedence

from .formatters import err_msg_formatter, err_ctx_formatter
from .importer import build_modules_registry
from .matchers import build_matchers
from .messages import EMPTY_EXPRESSION_PROVIDED, SYNTAX_ERROR
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
        except ParserGenericError as exc:

            # ’unwrap’ an original exception if that one has a stored context ??

            # print('wrapper :', type(exc))
            # print('original:', type(exc.__cause__))

            exc = exc.__cause__ if hasattr(exc.__cause__, 'ctx') else exc
            ctx = exc.ctx

            # print(exc)
            # print(ctx)

            # print(exc.__cause__.ctx)
            # print(ctx)
            # print(exc.__cause__.ctx)

            err_msg = err_msg_formatter(f'{SYNTAX_ERROR}')
            ctx_msg = err_ctx_formatter(ctx)
            # print(type(exc), exc, exc.ctx)
            # print(exc.__cause__)

            return f'{err_msg}\n{ctx_msg}'

        # except (ArithmeticError, ZeroDivisionError) as exc:
        #     print(type(exc), exc)
        #     err_msg = err_msg_formatter(exc)
        #     return err_msg

        except Exception as exc:
            print(type(exc), exc)
            print(f'CALCULATOR: exception: {exc}')
            return 'Calculation failed.'


def calculator(modules_names=None):
    """Initialize of a calculator and return a parser object."""

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


# TODO: remove
if __name__ == "__main__":
    import math

    def logger(fn):
        def wrap(source):
            print('=' * 30)
            print(f'input : {source}')
            result = fn(source)
            print(f'output: {result}')
            return result
        return wrap

    p = calculator()
    p.parse = logger(p.calculate)

    assert p.parse('sin(2)') == math.sin(2)
    assert p.parse('sin(2-3)') == math.sin(2 - 3)
    assert p.parse('2') == 2
    assert p.parse('    2') == 2
    assert p.parse('- 2') == - 2
    assert p.parse('- - 2') == 2
    assert p.parse('1 - 2') == -1
    assert p.parse('    1    -    2   ') == -1
    assert p.parse('1 - - 2') == 3
    assert p.parse('1 - - - 2  ') == -1
    assert p.parse('2 ^ 3 ') == 8
    assert p.parse('1 - 2 * 3') == -5
    assert p.parse('3 ^ 2 * 2') == 18
    assert p.parse('3 * 2 ^ 2') == 12
    assert p.parse('4 ^ 3 ^ 2') == 262144
    assert p.parse('6-(-13)') == 19
    assert p.parse('( 7 - 2 ) * 3') == 15
    assert p.parse('(0)') == 0
    assert p.parse('0 > 1') is False
    assert p.parse('0 >= 1') is False
    assert p.parse('2 > 1') is True
    assert p.parse('1 >= 1') is True
    assert p.parse('1 - 2 >= -1') is True
    assert p.parse('log(1025 - 1, 7 - 5)') == 10
    assert p.parse('1 + tau') == 1 + math.tau
    assert p.parse('1 + inf') == math.inf
    assert p.parse('1 - inf') == -math.inf
    assert p.parse('-inf + 1') == -math.inf
    assert str(p.parse('-inf + inf')) == str(math.nan)

    assert p.parse('1 / (1-1) + 1')       # ZeroDivisionError
    assert p.parse('100^100^100^100')     # OverflowError
    assert p.parse('sin(1,2)')
    assert p.parse(', 1')                 # from nud
    assert p.parse(') 2 ')                # from nud
    assert p.parse('1 , 2')               # not parsed completely
    assert p.parse('(2')                  # expected
    assert p.parse('sin2')                # expected
    assert p.parse('0 1')
    assert p.parse('a')                   # expected token in expr begin

    # asserts from pycalc_checker.py error cases
    p.parse('+')
    p.parse('1-')
    p.parse('1 2')
    p.parse('==7')
    p.parse('1+2(3*4))')
    p.parse('((1+2)')
    p.parse('1+1 2 3 4 5 6')
    p.parse('log100(100)')
    p.parse('------')
    p.parse('5> =6')
    p.parse('5/ /6')
    p.parse('6<=6')
    p.parse('6* *6')
    p.parse('(((((')
    p.parse('abs')
    p.parse('pow(2, 3, 4)')

    p.parse('1 / 0')
    p.parse('10 ^ 10 ^ 10 ^ 10')
