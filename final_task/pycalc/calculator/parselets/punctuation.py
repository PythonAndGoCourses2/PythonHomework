"""
The punctuation parselets.
"""

from .base import Base


class Comma(Base):
    """The parselet class for comma."""

    def nud(self, parser, token):
        """"""

        return parser.expression(self.power)
