"""

"""

from math import pow as math_pow
import math  # TODO: remove

from pycalc.specification.specification import ParserSpecification

from pycalc.token.constants import TokenType
from pycalc.token.precedence import Precedence
from pycalc.token.tokens import *

# FIX: operator build and Operator from token same name
import operator


def build_specification(registry):

    spec = ParserSpecification()

    # NUMBERS
    spec.nud.register(TokenType.NUMERIC, Number,
                      power=Precedence.DEFAULT)

    # FUNCTIONS
    spec.nud.register(TokenType.FUNCTION, Function,
                      power=Precedence.CALL,
                      func_registry=registry['functions'],
                      start=TokenType.LEFT_PARENTHESIS,
                      stop=TokenType.RIGHT_PARENTHESIS,
                      sep=TokenType.COMMA)

    # OPERATIONS

    # positive
    spec.nud.register(TokenType.ADD, UnaryPrefix,
                      power=Precedence.POSITIVE,
                      func=lambda x: +x)
    # negation
    spec.nud.register(TokenType.SUB, UnaryPrefix,
                      power=Precedence.NEGATIVE,
                      func=lambda x: -x)

    # addition
    spec.led.register(TokenType.ADD, BinaryInfixLeft,
                      power=Precedence.ADDITION,
                      func=operator.add)
    # subtraction
    spec.led.register(TokenType.SUB, BinaryInfixLeft,
                      power=Precedence.SUBTRACTION,
                      func=operator.sub)

    # exponentiation
    spec.led.register(TokenType.POW, BinaryInfixRight,
                      power=Precedence.EXPONENTIATION,
                      func=math_pow)

    # multiplication
    spec.led.register(TokenType.MUL, BinaryInfixLeft,
                      power=Precedence.MULTIPLICATION,
                      func=operator.mul)

    # division
    spec.led.register(TokenType.TRUEDIV, BinaryInfixLeft,
                      power=Precedence.DIVISION,
                      func=operator.truediv)

    # remainder
    spec.led.register(TokenType.MOD, BinaryInfixLeft,
                      power=Precedence.REMAINDER,
                      func=operator.mod)

    # equal or greater
    spec.led.register(TokenType.EQ, BinaryInfixLeft,
                      power=Precedence.COMPARISONS,
                      func=operator.eq)

    # greater
    spec.led.register(TokenType.GT, BinaryInfixLeft,
                      power=Precedence.COMPARISONS,
                      func=operator.gt)

    # equal or greater
    spec.led.register(TokenType.GE, BinaryInfixLeft,
                      power=Precedence.COMPARISONS,
                      func=operator.ge)

    # PUNCTUATION
    spec.nud.register(TokenType.LEFT_PARENTHESIS, GroupedExpressionStart,
                      power=Precedence.BINDING,
                      right_pair=TokenType.RIGHT_PARENTHESIS)

    spec.led.register(TokenType.RIGHT_PARENTHESIS, GroupedExpressionEnd,
                      power=Precedence.DEFAULT)

    spec.led.register(TokenType.COMMA, Comma,
                      power=Precedence.DEFAULT)

    return spec
