"""
Parser specification.
"""

from .led import Led
from .nud import Nud


class Specification:
    """
    Holds nud and led.
    """

    def __init__(self):
        self.nud = Nud()
        self.led = Led()
