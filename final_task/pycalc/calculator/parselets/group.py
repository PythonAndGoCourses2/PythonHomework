"""
The parselet classes for grouped expressions.
"""

from .base import Base


class GroupedExpressionStart(Base):
    """A grouped expression start parselet."""

    def __init__(self, power, right_pair):
        super().__init__(power)
        self.right_pair = right_pair

    def nud(self, parser, token):
        """"""

        expr = parser.expression()
        parser.advance(self.right_pair)

        return expr


class GroupedExpressionEnd(Base):
    """A grouped expression end parselet."""

    def led(self, parser, token, left):
        """"""

        return parser.expression(self.power)
