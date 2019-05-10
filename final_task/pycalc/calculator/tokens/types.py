"""
Token types specification.
"""


from enum import Enum, auto


class TokenType(Enum):
    """Token types specification."""

    NUMERIC = auto()    # 0 1 2.3 4. .5, ...  (TODO: 3.14e-10 3.14j ?)
    CONSTANT = auto()   # e, pi, ...
    FUNCTION = auto()   # abs, sin, ...

    # operators
    ADD = auto()        # +
    SUB = auto()        # -
    MUL = auto()        # *
    TRUEDIV = auto()    # /
    FLOORDIV = auto()   # //
    POW = auto()        # ^
    MOD = auto()        # %

    # comparison operators
    EQ = auto()         # ==
    NE = auto()         # !=
    LT = auto()         # <
    LE = auto()         # <=
    GT = auto()         # >
    GE = auto()         # >

    # built-in functions
    ABS = auto()        # abs
    ROUND = auto()      # round

    # punctuation
    COMMA = auto()  # ,
    LEFT_PARENTHESIS = auto()  # (
    RIGHT_PARENTHESIS = auto()  # )
