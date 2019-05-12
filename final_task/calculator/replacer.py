# -*- coding: utf-8 -*-
"""
The module is intended to replace mathematical expressions with their result.

Example:
        replace_unary_operator('1+-+-+-3')
        >>> '1-3'

        lib = {
            'e': 2.718281828459045,
            'sum': sum
        }
        replace_constant('1+e', lib)
        >>> '1+2.718281828459045'

        replace_fanction('sum(100,50)', lib)
        >>> '150'
"""

import re
from collections import namedtuple
from functools import reduce
import regexp as mre
from library import Library
from operators import LEFT_BRACKET, MINUS, PLUS, MULTIPLE, POWER, TRUE_DIVISION, FLOOR_DIVISION, MODULE, \
                      EQUAL, NOT_EQUAL, GREAT, GREAT_OR_EQUAL, LESS, LESS_OR_EQUAL, exec_operation


def replace_constant(expr: str, library: Library) -> str:
    """
    Calculates constant operations.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.finditer(mre.REGEXP_CONSTANT, expr)

    for m in results:
        name = m.group('name')

        if name[-1] == LEFT_BRACKET or re.match(mre.REGEXP_DIGIT, name):
            continue

        answer = str(library[name])
        arr = expr.split(name)

        for idx, piece in enumerate(arr[:-1]):
            if piece and piece[-1].isalnum():
                arr[idx] = f'{piece}{name}'
            elif piece or not idx:
                arr[idx] = f'{piece}{answer}'

        expr = ''.join(arr)

    return expr


def replace_fanction(expr: str, library: Library) -> str:
    """
    Calculates function operations.

    Args:
        expr (str): String mathematical expression.
        library (Library): dictionary of functions and constant.

    Returns:
        str: Updated expression.
    """
    results = re.finditer(mre.REGEXP_FUNCTION, expr)

    for m in results:
        func = m.group('name')
        pattern = m.group('pattern')
        args = filter(bool, m.group('args').split(','))
        args = [float(v) for v in args]
        answer = str(library[func](*args))
        expr = expr.replace(pattern, answer)

    return expr


def replace_unary_operator(expr: str) -> str:
    """
    Calculates unary operations.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.findall(mre.REGEXP_UNARY, expr)
    results.sort(key=len, reverse=True)

    for m in results:
        answer = MINUS if m.count(MINUS) % 2 else PLUS
        expr = expr.replace(m, answer)

    return expr


def replace_compare_operator(expr: str, *operations: list) -> str:
    """
    Calculates compare operations.

    Args:
        expr (str): String mathematical expression.
        *operations (list): List of operations that need to be done on the expression.

    Returns:
        str: Updated expression.
    """
    if re.search(mre.REGEXP_COMPARE, expr):
        return replace_bynary_operator(expr, *operations)

    return expr


def replace_bynary_operator(expr: str, *operations: list) -> str:
    """
    Calculates binary operations.

    Args:
        expr (str): String mathematical expression.
        *operations (list): List of operations that need to be done on the expression.

    Returns:
        str: Updated expression.
    """
    for o in operations:
        delimeter = o
        if o == PLUS or o == MULTIPLE or o == POWER:
            delimeter = mre.REGEXP_SCREENING.format(operation=o)

        regexp = mre.REGEXP_BYNARY.format(operation=delimeter)
        results = re.findall(regexp, expr)
        for m in results:
            arr = list(filter(bool, m.split(o)))
            if o == MINUS and m[0] == MINUS:
                arr[0] = f'{MINUS}{arr[0]}'
            if o == POWER:
                arr = arr[::-1]

            answer = reduce(lambda a, b: exec_operation(a, b, operation=o), arr)
            expr = expr.replace(m, answer)

    return expr


def replace_brackets(expr: str, library: Library) -> str:
    """
    Calculates the expression in brackets.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.findall(mre.REGEXP_BACKETS, expr)

    for m in results:
        answer = replace_all_mathes(m[1:-1], library)
        expr = expr.replace(m, answer)

    return expr


def replace_all_mathes(expr: str, library: Library) -> str:
    """
    Calculates the result from the getting expression.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: result of calculations.
    """
    Operation = namedtuple('Operation', 'func args')
    OPERATION_PRIORITY = [
        Operation(replace_constant, [library]),
        Operation(replace_fanction, [library]),
        Operation(replace_brackets, [library]),
        Operation(replace_unary_operator, []),
        Operation(replace_bynary_operator, [POWER]),
        Operation(replace_bynary_operator, [MULTIPLE, TRUE_DIVISION, FLOOR_DIVISION, MODULE]),
        Operation(replace_bynary_operator, [PLUS, MINUS]),
        Operation(replace_compare_operator, [EQUAL, NOT_EQUAL, GREAT, GREAT_OR_EQUAL, LESS, LESS_OR_EQUAL]),
    ]

    pattern = re.compile(mre.REGEXP_SIMPLE_DIGIT)
    while True:
        for inst in OPERATION_PRIORITY:
            expr = inst.func(expr, *inst.args)
            if pattern.match(expr):
                return expr

    return expr
