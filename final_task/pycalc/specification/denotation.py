"""
Denotation.
"""


class _Denotation:
    """
    The base class for nud- and led-denotation classes.
    """

    def __init__(self):
        self.registry = {}

    def register(self, token_type, parselet, **kwargs):
        """
        Register token type with an appropriate parselet.
        """
        self._check_for_dup(token_type)
        self.registry[token_type] = parselet(**kwargs)

    def power(self, token):
        """
        Return power for a given token.
        """

        power = self._get_parselet(token).power

        return power

    def _get_parselet(self, token):
        """
        Find and return stored parselet for a given token.
        """

        token_type = token.token_type

        try:
            parselet = self.registry[token_type]
        except KeyError:
            raise SyntaxError(f'not in specification: {token_type}')

        return parselet

    def _check_for_dup(self, token_type):
        """
        Check if a givent token type is already registered.
        """

        if token_type in self.registry:
            raise Exception(
                f'Token of {token_type} type is already registered.')


class Nud(_Denotation):
    """
    Null-Denotation.

    The specification of how an operator consumes to the right with no left-context.
    """

    def eval(self, parser, token):
        """
        Evaluate and return result.
        """

        parselet = self._get_parselet(token)
        result = parselet.nud(parser, token)

        return result


class Led(_Denotation):
    """
    Left-Denotation.

    The specification of how an operator consumes to the right with a left-context.
    """

    def eval(self, parser, token, left):
        """
        Evaluate and return result.
        """

        parselet = self._get_parselet(token)
        result = parselet.led(parser, token, left)

        return result


if __name__ == "__main__":
    from collections import namedtuple
    from pycalc.token.constants import TokenType, Predefined
    from pycalc.token.description import PREDEFINED_TOKEN_DESC
    from pycalc.token.precedence import Precedence
    from pycalc.token.tokens import Number

    Token = namedtuple("Token", ("token_type", "lexeme"))

    token = Token('op', '+')
    d = _Denotation()
