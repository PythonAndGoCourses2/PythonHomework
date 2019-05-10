"""
Lexemes.
"""

from itertools import chain

from .types import TokenType


PREDEFINED = {
    # common operators
    TokenType.ADD: '+',
    TokenType.SUB: '-',
    TokenType.MUL: '*',
    TokenType.TRUEDIV: '/',
    TokenType.FLOORDIV: '//',
    TokenType.POW: '^',
    TokenType.MOD: '%',

    # comparison operators
    TokenType.EQ: '==',
    TokenType.NE: '!=',
    TokenType.LT: '<',
    TokenType.LE: '<=',
    TokenType.GT: '>',
    TokenType.GE: '>=',

    # built-in functions
    TokenType.ABS: 'abs',
    TokenType.ROUND: 'round',

    # punctuation
    TokenType.COMMA: ',',
    TokenType.LEFT_PARENTHESIS: '(',
    TokenType.RIGHT_PARENTHESIS: ')',
}

# lexemes for this token types are created dynamically at runtime
DYNAMIC = (
    TokenType.NUMERIC,
    TokenType.FUNCTION,
    TokenType.CONSTANT,
)

ALL = (PREDEFINED, DYNAMIC)


# Simple import time validations (TODO: not for production, to refactor)

# all non-dynamically created token types should have lexemes
for token_type in TokenType:
    if token_type not in chain(*ALL):
        raise Exception(f'no lexeme is specified for {token_type}')
