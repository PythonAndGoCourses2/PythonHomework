"""
Left-Denotation.
"""

from .denotation import Denotation
from .errors import LedDenotationError, ParseletNotRegistered


class Led(Denotation):
    """
    Left-Denotation.

    The specification of how an operator consumes to the right with a left-context.
    """

    def power(self, parser, token):
        """Return power for a given token."""

        parselet = self._parselet(parser, token)
        power = parselet.power

        return power

    def eval(self, parser, token, left):
        """Receive from left, evaluate and return result."""

        parselet = self._parselet(parser, token)
        result = parselet.led(parser, token, left)

        return result

    def _parselet(self, parser, token):
        """Find and return a stored parselet for a given token type."""

        try:
            parselet = super()._get_parselet(token)
        except ParseletNotRegistered:
            ctx = parser.context()
            raise LedDenotationError(ctx, token)

        return parselet
