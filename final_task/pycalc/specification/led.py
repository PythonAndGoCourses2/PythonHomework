"""
Left-Denotation.
"""

from .denotation import Denotation


class Led(Denotation):
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
