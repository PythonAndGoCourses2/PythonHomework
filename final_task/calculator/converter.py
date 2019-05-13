# -*- coding: utf-8 -*-
"""
The module is designed to convert the expression to the desired type.

Example:
        convert_answer('-1', False)
        >>> '-1'

        convert_answer('-1', False)
        >>> '0'

        convert_answer('-1', True)
        >>> 'True'

        convert_answer('0', True)
        >>> 'False'
"""

from .regexp import has_non_zero_fraction_part


def convert_answer(expr: str, has_compare: bool) -> str:
    """
    Converts the resulting string to the desired type.

    Args:
        expr (str): String representation of a number.
        has_compare (bool): whether the expression contains boolean logic
    """
    num = float(expr)
    match = has_non_zero_fraction_part(expr)
    num = num if match else int(num)

    result = bool(num) if has_compare else num

    return str(result)
