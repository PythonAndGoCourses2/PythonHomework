"""
Initialization of a calculator. Returns a parser object.
"""

from pycalc.lexer import Lexer
from pycalc.parser import Parser

from .importer import build_modules_registry
from .matchers import build_matchers
from .specification import build_specification


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
    parser = Parser(spec, lexer)

    return parser


# TODO: remove
if __name__ == "__main__":
    import math

    p = calculator()

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

    # assert p.parse('1 / 0')
    # assert p.parse('sin(1,2)')
    # assert p.parse(', 1')
    # assert p.parse('1 , 2')
    # assert p.parse(') 2 ') == 15
    # assert p.parse('0 1')
    # assert p.parse('- - - 2 ^ log ( 1 , ( 4 - 1 ) * 5 , 4 )') == -1048576
    # TODO:
