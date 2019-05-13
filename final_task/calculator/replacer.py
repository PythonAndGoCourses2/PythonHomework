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
from .library import Library
from .operators import (
    LEFT_BRACKET,
    MINUS,
    PLUS,
    MULTIPLE,
    POWER,
    TRUE_DIVISION,
    FLOOR_DIVISION,
    MODULE,
    EQUAL,
    NOT_EQUAL,
    GREAT,
    GREAT_OR_EQUAL,
    LESS,
    LESS_OR_EQUAL,
    exec_operation,
)
from .regexp import (
    REGEXP_BACKETS,
    REGEXP_CONSTANT,
    REGEXP_DIGIT,
    REGEXP_SCREENING,
    REGEXP_BYNARY,
    REGEXP_COMPARE,
    REGEXP_UNARY,
    REGEXP_FUNCTION,
    REGEXP_SIMPLE_DIGIT,
)


def replace_constant(expr: str, library: Library) -> str:
    """
    Calculates constant operations.

    Args:
        expr (str): String mathematical expression.
        library (Library): dictionary of functions and constant.

    Returns:
        str: Updated expression.
    """
    matches = re.finditer(REGEXP_CONSTANT, expr)

    for match in matches:
        name = match.group('name')

        if name[-1] == LEFT_BRACKET or re.match(REGEXP_DIGIT, name):
            continue

        result = str(library[name])
        arr = expr.split(name)

        for idx, piece in enumerate(arr[:-1]):
            if piece and piece[-1].isalnum():
                arr[idx] = f'{piece}{name}'
            elif piece or not idx:
                arr[idx] = f'{piece}{result}'

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
    matches = re.finditer(REGEXP_FUNCTION, expr)

    for match in matches:
        func = match.group('name')
        pattern = match.group('pattern')
        args = filter(bool, match.group('args').split(','))
        args = [float(v) for v in args]
        result = str(library[func](*args))
        expr = expr.replace(pattern, result)

    return expr


def replace_unary_operator(expr: str) -> str:
    """
    Calculates unary operations.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    matches = re.findall(REGEXP_UNARY, expr)
    matches.sort(key=len, reverse=True)

    for match in matches:
        result = MINUS if match.count(MINUS) % 2 else PLUS
        expr = expr.replace(match, result)

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
    if re.search(REGEXP_COMPARE, expr):
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
    for operation in operations:
        delimeter = operation
        if operation == PLUS or operation == MULTIPLE or operation == POWER:
            delimeter = REGEXP_SCREENING.format(operation=operation)

        regexp = REGEXP_BYNARY.format(operation=delimeter)
        matches = re.findall(regexp, expr)
        for match in matches:
            operands = list(filter(bool, match.split(operation)))
            if operation == MINUS and match[0] == MINUS:
                operands[0] = f'{MINUS}{operands[0]}'
            if operation == POWER:
                operands = operands[::-1]

            result = reduce(lambda acc, val: exec_operation(acc, val, operation=operation), operands)
            expr = expr.replace(match, result)

    return expr


def replace_brackets(expr: str, library: Library) -> str:
    """
    Calculates the expression in brackets.

    Args:
        expr (str): String mathematical expression.
        library (Library): dictionary of functions and constant.

    Returns:
        str: Updated expression.
    """
    matches = re.findall(REGEXP_BACKETS, expr)

    for match in matches:
        result = replace_all_mathes(match[1:-1], library)
        expr = expr.replace(match, result)

    return expr


def replace_all_mathes(expr: str, library: Library) -> str:
    """
    Calculates the result from the getting expression.

    Args:
        expr (str): String mathematical expression.
        library (Library): dictionary of functions and constant.

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

    pattern = re.compile(REGEXP_SIMPLE_DIGIT)
    while True:
        for operation in OPERATION_PRIORITY:
            expr = operation.func(expr, *operation.args)
            if pattern.match(expr):
                return expr

    return expr
