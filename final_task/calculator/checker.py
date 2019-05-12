# -*- coding: utf-8 -*-
"""
The module is designed to test the mathematical expression for correctness.

Example:
        check_spaces(' 1+ 3 / 2')
        >>> '1+3/2'

        check_brackets('2*(3+5)')
        >>> '2*(3+5)'

        lib = {
            'e': 2.718281828459045,
            'sum': sum
        }
        check_function('sum(100, 50)', lib)
        >>> 'sum(100, 50)'
"""

import re
import regexp as mre
from operators import LEFT_BRACKET, RIGHT_BRACKET
from library import Library


def check_spaces(expr: str) -> str:
    """
    Checks if an expression has the wrong elements.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: cleared expression from spaces.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    res = re.findall(mre.REGEXP_INCORECT_EXPRETION, expr)
    if res:
        raise ValueError('expression is not correct')

    return expr.replace(' ', '')


def check_brackets(expr: str):
    """
    Checks if all brackets have a pair.

    Args:
        expr (str): String mathematical expression.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    stack = []
    for c in expr:
        if c == LEFT_BRACKET:
            stack.append(c)
        elif c == RIGHT_BRACKET and (not stack or stack.pop() != LEFT_BRACKET):
            raise ValueError('brackets are not balanced')

    if stack:
        raise ValueError('brackets are not balanced')


def check_constant(expr: str, library: Library):
    """
    Checks if all constants in the expression are available.

    Args:
        expr (str): String mathematical expression.
        library (Library): dictionary of functions and constant.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    results = re.finditer(mre.REGEXP_CONSTANT, expr)
    for m in results:
        name = m.group('name')

        if name[-1] == LEFT_BRACKET or re.match(mre.REGEXP_DIGIT, name):
            continue

        if name[0].isdigit():
            raise ValueError(f'constant {name} can not start with digit')

        if name not in library or callable(library[name]):
            raise ValueError(f'there is no such constant {name}')


def check_function(expr: str, library: Library):
    """
    Checks if all functions in the expression are available.

    Args:
        expr (str): String mathematical expression.
        library (Library): dictionary of functions and constant.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    results = re.finditer(mre.REGEXP_FUNCTION, expr)
    for m in results:
        name = m.group('name')
        pattern = m.group('pattern')

        if name[0].isdigit():
            raise ValueError(f'function {pattern} can not start with digit')

        if name not in library or not callable(library[name]):
            raise ValueError(f'there is no such function {pattern}')


def check_expression(expr: str, library: Library) -> str:
    """
    Checks the expression for correctness.

    Args:
        expr (str): String mathematical expression.
        library (Library): dictionary of functions and constant.

    Returns:
        str: cleared expression.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    expr = check_spaces(expr)
    check_brackets(expr)
    check_constant(expr, library)
    check_function(expr, library)

    return expr
