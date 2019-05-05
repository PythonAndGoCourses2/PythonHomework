"""
Parser Specification
"""

from .denotation import Nud, Led


class ParserSpecification:
    """
    Hold nud and led.
    """

    def __init__(self):
        self.nud = Nud()
        self.led = Led()

#


from pycalc.token.constants import TokenType
from pycalc.token.tokens import *
from pycalc.token.precedence import Precedence
import operator
from math import pow as math_pow

spec = ParserSpecification()

# NUMBERS
spec.nud.register(TokenType.NUMERIC, Number,
                  power=Precedence.DEFAULT)

# OPERATIONS

# negation
spec.nud.register(TokenType.SUB, UnaryPrefix,
                  power=Precedence.NEGATIVE,
                  func=lambda x: -x)

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

spec.led.register(TokenType.GE, BinaryInfixLeft,
                  power=Precedence.COMPARISONS,
                  func=operator.ge)

spec.led.register(TokenType.GT, BinaryInfixLeft,
                  power=Precedence.COMPARISONS,
                  func=operator.gt)

# FUNCTIONS

# sum
spec.nud.register(TokenType.SUM, Function,
                  power=Precedence.CALL,
                  func=sum,
                  start=TokenType.LEFT_PARENTHESIS,
                  stop=TokenType.RIGHT_PARENTHESIS,
                  sep=TokenType.COMMA)

# PUNCTUATION
spec.nud.register(TokenType.LEFT_PARENTHESIS, GroupedExpressionStart,
                  power=Precedence.BINDING,
                  right_pair=TokenType.RIGHT_PARENTHESIS)

spec.led.register(TokenType.RIGHT_PARENTHESIS, GroupedExpressionEnd,
                  power=Precedence.DEFAULT)

spec.led.register(TokenType.COMMA, Comma,
                  power=Precedence.DEFAULT)
