"""
Build matchers.
"""

from pycalc.matcher.matcher import Matchers
from pycalc.matcher.number import NUMBER_MATCHER
from pycalc.token.constants import TokenType


PREDEFINED_MATCHERS = {
    TokenType.NUMERIC: NUMBER_MATCHER
}


def build_matchers(registry):
    """"""

    matchers = Matchers()

    matchers.register_matcher(TokenType.NUMERIC,
                              PREDEFINED_MATCHERS[TokenType.NUMERIC])

    matchers.register_matcher(TokenType.FUNCTION,
                              matchers.create_from.literals_list(
                                  registry['functions'].keys())
                              )

    matchers.register_matcher(TokenType.CONSTANT,
                              matchers.create_from.literals_list(
                                  registry['constants'].keys())
                              )

    matchers.register_matcher(TokenType.ADD,
                              matchers.create_from.literals_list(['+']))

    matchers.register_matcher(TokenType.SUB,
                              matchers.create_from.literals_list(['-']))

    matchers.register_matcher(TokenType.MUL,
                              matchers.create_from.literals_list(['*']))

    matchers.register_matcher(TokenType.TRUEDIV,
                              matchers.create_from.literals_list(['/']))

    matchers.register_matcher(TokenType.MOD,
                              matchers.create_from.literals_list(['%']))

    matchers.register_matcher(TokenType.POW,
                              matchers.create_from.literals_list(['^']))

    matchers.register_matcher(TokenType.EQ,
                              matchers.create_from.literals_list(['==']))

    matchers.register_matcher(TokenType.NE,
                              matchers.create_from.literals_list(['!=']))

    matchers.register_matcher(TokenType.GE,
                              matchers.create_from.literals_list(['>=']))

    matchers.register_matcher(TokenType.GT,
                              matchers.create_from.literals_list(['>']))

    matchers.register_matcher(TokenType.LEFT_PARENTHESIS,
                              matchers.create_from.literals_list(['(']))

    matchers.register_matcher(TokenType.RIGHT_PARENTHESIS,
                              matchers.create_from.literals_list([')']))

    matchers.register_matcher(TokenType.COMMA,
                              matchers.create_from.literals_list([',']))

    return matchers
