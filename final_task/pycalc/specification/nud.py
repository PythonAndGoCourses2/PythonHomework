"""
Null-Denotation.
"""

from .denotation import Denotation


class Nud(Denotation):
    """
    Null-Denotation.

    The specification of how an operator consumes to the right with no left-context.
    """

    def eval(self, parser, token):
        """Evaluate and return result."""

        parselet = self._get_parselet(token)
        result = parselet.nud(parser, token)

        return result
