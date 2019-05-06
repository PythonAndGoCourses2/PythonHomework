"""
Parser specification.
"""

from .denotation import Nud, Led


class ParserSpecification:
    """
    Holds nud and led.
    """

    def __init__(self):
        self.nud = Nud()
        self.led = Led()
