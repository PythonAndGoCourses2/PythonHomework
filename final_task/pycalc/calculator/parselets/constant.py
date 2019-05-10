"""
The parselet class for constants.
"""

from .base import Base


class Constant(Base):
    """The parselet class for constants."""

    def __init__(self, power, const_registry):
        super().__init__(power)
        self.const_registry = const_registry

    def nud(self, parser, token):
        """"""

        const = self.const(token)

        return const

    def const(self, token):
        """"""

        const_name = token.lexeme
        try:
            const = self.const_registry[const_name]
        except KeyError:
            raise Exception(f"$'{const_name}' constant is not registered")

        return const
