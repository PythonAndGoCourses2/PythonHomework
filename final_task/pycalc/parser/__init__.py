"""
Parser package provides a Parser class for
top down operator precedence parcing (Pratt parser).

https://en.wikipedia.org/wiki/Pratt_parser
"""

from .parser import Parser
from .errors import (
    ParserGenericError,
    ParserNoTokenReceived,
    ParserExpectedTokenAbsent,
    ParserSourceNotExhausted
)
