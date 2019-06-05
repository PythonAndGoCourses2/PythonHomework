"""
Specification for top down operator
precedence parsing (Pratt parser).
"""

from .specification import Specification
from .errors import (
    DuplicatedTokenType,
    NudDenotationError,
    LedDenotationError
)
