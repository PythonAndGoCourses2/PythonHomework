"""
Create and register matchers for token types.
"""


from pycalc.matcher import Matchers

from .tokens.types import TokenType
from .tokens.lexemes import PREDEFINED


def build_matchers(imports_registry):
    """Create and register matchers for token types."""

    matchers = Matchers()

    # create matchers for token types with dynamically created lexemes

    numeric_matcher = matchers.create_from.compiled_regex(NUMBER_REGEX)

    functions_matcher = matchers.create_from.literals_list(
        imports_registry['functions'].keys())

    constants_matcher = matchers.create_from.literals_list(
        imports_registry['constants'].keys())

    # register matchers for token types with dynamically created lexemes
    matchers.register_matcher(TokenType.NUMERIC, numeric_matcher)
    matchers.register_matcher(TokenType.FUNCTION, functions_matcher)
    matchers.register_matcher(TokenType.CONSTANT, constants_matcher)

    # sort predefined lexemes map by lexeme length in reversed order
    lexemes_map = sorted(PREDEFINED.items(),
                         key=lambda kv: len(kv[1]),
                         reverse=True)

    # create and register matchers for predefined lexemes
    for token_type, lexeme in lexemes_map:
        matchers.register_matcher(token_type,
                                  matchers.create_from.literals_list([lexeme]))

    return matchers
