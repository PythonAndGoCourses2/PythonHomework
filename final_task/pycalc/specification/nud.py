"""
Null-Denotation.
"""

from .denotation import Denotation
from .errors import NudDenotationError


class Nud(Denotation):
    """
    Null-Denotation.

    The specification of how an operator consumes to the right with no left-context.
    """

    def eval(self, parser, token):
        """Evaluate and return result."""

        try:
            parselet = self._get_parselet(token)
        except KeyError:
            ctx = parser.context(previous=True)
            raise NudDenotationError(ctx, token)

        result = parselet.nud(parser, token)

        return result
