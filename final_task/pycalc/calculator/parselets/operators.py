"""
The parselet classes for operations.
"""

from .base import Base
from .helpers import call


class Operator(Base):
    """The generic parselet class for operations."""

    def __init__(self, power, func):
        super().__init__(power)
        self.func = func


class UnaryPrefix(Operator):
    """The parselet class for unary prefix operations."""

    def nud(self, parser, token):
        """"""

        ctx = parser.context(previous=True)

        right = parser.expression(self.power)
        result = call(ctx, self.func, [right])

        return result


class UnaryPostfix(Operator):
    """The parselet class for unary postfix operations."""

    def led(self, parser, token, left):
        """"""

        ctx = parser.context(previous=True)

        result = call(ctx, self.func, [left])

        return result


class BinaryInfixLeft(Operator):
    """The parselet class for binary prefix operations."""

    def led(self, parser, token, left):
        """"""

        ctx = parser.context(previous=True)

        right = parser.expression(self.power)
        result = call(ctx, self.func, [left, right])

        return result


class BinaryInfixRight(Operator):
    """The parselet class for binary infix operations."""

    def led(self, parser, token, left):
        """"""

        ctx = parser.context(previous=True)

        right = parser.expression(self.power - 1)
        result = call(ctx, self.func, [left, right])

        return result
