"""
Provides the base class for nud- and led-denotation classes.
"""

from .errors import DuplicatedTokenType, ParseletNotRegistered


class Denotation:
    """
    The base class for nud- and led-denotation classes.
    """

    def __init__(self):
        self.registry = {}

    def register(self, token_type, parselet, **kwargs):
        """Register a parselet for a given token type."""

        self._check_for_dup(token_type)
        self.registry[token_type] = parselet(**kwargs)

    def _get_parselet(self, token):
        """Find and return a parselet for a given token type."""

        token_type = token.token_type
        try:
            parselet = self.registry[token_type]
        except KeyError:
            raise ParseletNotRegistered(token_type)

        return parselet

    def _check_for_dup(self, token_type):
        """
        Check if a givent token type is already registered.
        """

        if token_type in self.registry:
            raise DuplicatedTokenType(token_type)
