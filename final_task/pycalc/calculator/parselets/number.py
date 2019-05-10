"""
The parselet class for numbers.
"""

from .base import Base


class Number(Base):
    """The parselet class for numbers."""

    def nud(self, parser, token):
        """"""

        try:
            value = int(token.lexeme)
        except ValueError:
            value = float(token.lexeme)

        return value
