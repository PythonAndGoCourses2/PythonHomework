"""
The operator precedence.
"""

from enum import IntEnum


class Precedence(IntEnum):
    """
    The operator precedence according to the operator precedence in Python.

    https://docs.python.org/3/reference/expressions.html#operator-precedence
    """
    DEFAULT = 0

    # Lambda expression
    LAMBDA = 10                     # lambda
    # Conditional expression
    CONDITIONAL_EXPRESSION = 20     # if – else
    # Boolean OR
    BOOLEAN_OR = 30                 # or
    # Boolean AND
    BOOLEAN_AND = 40                # and
    # Boolean NOT
    BOOLEAN_NOT = 50                # not x

    # Comparisons, including membership tests and identity tests
    COMPARISONS = 60                # <, <= , > , >= , != , ==
    MEMBERSHIP_TESTS = 60           # in, not in
    IDENTITY_TESTS = 60             # is, is not

    # Bitwise XOR
    BITWISE_XOR = 70                # ^
    # Bitwise OR
    BITWISE_OR = 80                 # |
    # Bitwise AND
    BITWISE_AND = 90                # &
    # Shifts
    SHIFTS = 100                    # <<, >>

    # Addition and subtraction
    ADDITION = 110                  # +
    SUBTRACTION = 110               # -

    # Multiplication, matrix multiplication, division, floor division, remainder
    MULTIPLICATION = 120            # *
    MATRIX_MULTIPLICATION = 120     # @
    DIVISION = 120                  # /
    FLOOR_DIVISION = 120            # //
    REMAINDER = 120                 # %

    # Positive, negative, bitwise NOT
    POSITIVE = 130                  # +x
    NEGATIVE = 130                  # -x
    BITWISE_NOT = 130               # ~x

    # Exponentiation
    EXPONENTIATION = 140            # ^
    # EXPONENTIATION = 140          # **

    # Await expression
    AWAIT = 150  # await x

    # Subscription, slicing, call, attribute reference
    SUBSCRIPTION = 160              # x[index],
    SLICING = 160                   # x[index:index],
    CALL = 160                      # x(arguments...),
    ATTRIBUTE_REFERENCE = 160       # x.attribute

    # Binding or tuple display, list display, dictionary display, set display
    BINDING = 170
    TUPLE = 170                     # (expressions...),
    LIST = 170                      # [expressions...],
    DICTIONARY = 170                # {key: value...},
    SET = 170                       # {expressions...}
