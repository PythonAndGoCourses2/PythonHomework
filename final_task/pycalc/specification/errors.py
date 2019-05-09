"""
Exceptions for the specification package.
"""


def denotation_err_msg(token, denotation_type):
    """Return a formatted message for denotation error excepcions."""

    return f'{token.token_type} is not registered or can’t be in the {denotation_type}-position.'


class DuplicatedTokenType(Exception):
    """Raise when a token type is already registered in a registry."""

    def __init__(self, token_type):
        super().__init__()
        self.token_type = token_type


class DenotationError(SyntaxError):
    """The generic exception class for denotation errors."""

    def __init__(self, ctx, token):
        super().__init__()
        self.ctx = ctx
        self.token = token


class NudDenotationError(DenotationError):
    """
    Raise when a token type is not registered in a specification
    or can’t be in the nud-position.
    """

    def __str__(self):
        return denotation_err_msg(self.token, 'nud')


class LedDenotationError(DenotationError):
    """
    Raise when a token type is not registered in a specification
    or can’t be in the led-position.
    """

    def __str__(self):
        return denotation_err_msg(self.token, 'led')
