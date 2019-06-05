"""
The generic parselet class.
"""


class Base():
    """The generic parselet class."""

    def __init__(self, power):
        self.power = power

    def __repr__(self):
        return self.__class__.__name__
