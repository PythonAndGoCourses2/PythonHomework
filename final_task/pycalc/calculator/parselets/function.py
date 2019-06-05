"""
The parselet class for functions.
"""

from .base import Base
from .helpers import call


class Function(Base):
    """The parselet class for functions."""

    def __init__(self, power, func_registry, start, stop, sep):
        super().__init__(power)
        self.func_registry = func_registry
        self.start = start
        self.stop = stop
        self.sep = sep

    def nud(self, parser, token):
        """"""

        ctx = parser.context(previous=True)

        parser.advance(self.start)
        args = self.args(parser)
        parser.advance(self.stop)

        func = self.func(token)
        result = call(ctx, func, args)

        return result

    def args(self, parser):
        """Advance a parser and collect an arguments list."""

        args = []

        if not parser.peek_and_check(self.stop):
            while True:
                args.append(parser.expression())
                if not parser.peek_and_check(self.sep):
                    break
                parser.advance(self.sep)

        return args

    def func(self, token):
        """Get a function from the function registry by a function name."""

        func_name = token.lexeme
        try:
            func = self.func_registry[func_name]
        except KeyError:
            raise Exception(f"$'{func_name}' function is not registered")

        return func
