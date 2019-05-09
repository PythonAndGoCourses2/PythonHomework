"""
Left-Denotation.
"""

from .denotation import Denotation
from .errors import LedDenotationError


class Led(Denotation):
    """
    Left-Denotation.

    The specification of how an operator consumes to the right with a left-context.
    """

    def eval(self, parser, token, left):
        """Receive from left, evaluate and return result."""

        try:
            parselet = self._get_parselet(token)
        except KeyError:
            ctx = parser.context(previous=True)
            raise LedDenotationError(ctx, token)

        result = parselet.led(parser, token, left)

        return result
