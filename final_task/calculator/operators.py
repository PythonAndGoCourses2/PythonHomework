# -*- coding: utf-8 -*-
"""
The module is designed to calculate mathematical operations. 
Also contains string representations of operations.

Attributes:
    LEFT_BRACKET (str): possible representation of the bracket ( in the expression.
    RIGHT_BRACKET (str): possible representation of the bracket ) in the expression.
    MULTIPLE (str): possible representation of the operation * in the expression.
    POWER (str): possible representation of the operation ** in the expression.
    TRUE_DIVISION (str): possible representation of the operation / in the expression.
    FLOOR_DIVISION (str): possible representation of the operation // in the expression.
    MODULE (str): possible representation of the operation % in the expression.
    PLUS (str): possible representation of the operation + in the expression.
    MINUS (str): possible representation of the operation - in the expression.
    LESS (str): possible representation of the operation < in the expression.
    LESS_OR_EQUAL (str): possible representation of the operation <= in the expression.
    GREAT (str): possible representation of the operation > in the expression.
    GREAT_OR_EQUAL (str): possible representation of the operation >= in the expression.
    EQUAL (str): possible representation of the operation == in the expression.
    NOT_EQUAL (str): possible representation of the operation != in the expression.
    Type (class): static class containing types of operations.
    OPERATORS (dict): key is string representation of operations, and value is namedtuple(func, type).
"""

import re
from collections import namedtuple
from operator import mul, truediv, floordiv, mod, add, sub, lt, le, eq, ne, ge, gt

LEFT_BRACKET = '('
RIGHT_BRACKET = ')'
MULTIPLE = '*'
POWER = '^'
TRUE_DIVISION = '/'
FLOOR_DIVISION = '//'
MODULE = '%'
PLUS = '+'
MINUS = '-'
LESS = '<'
LESS_OR_EQUAL = '<='
GREAT = '>'
GREAT_OR_EQUAL = '>='
EQUAL = '=='
NOT_EQUAL = '!='

class Type:
    ARITHMETIC = 0
    COMPARISON = 1

Operator = namedtuple('Operator', 'func type')
OPERATORS = {
    MULTIPLE: Operator(mul, Type.ARITHMETIC),
    POWER: Operator(pow, Type.ARITHMETIC),
    TRUE_DIVISION: Operator(truediv, Type.ARITHMETIC),
    FLOOR_DIVISION: Operator(floordiv, Type.ARITHMETIC),
    MODULE: Operator(mod, Type.ARITHMETIC),
    PLUS: Operator(add, Type.ARITHMETIC),
    MINUS: Operator(sub, Type.ARITHMETIC),
    LESS: Operator(lt, Type.COMPARISON),
    LESS_OR_EQUAL: Operator(le, Type.COMPARISON),
    EQUAL: Operator(eq, Type.COMPARISON),
    NOT_EQUAL: Operator(ne, Type.COMPARISON),
    GREAT_OR_EQUAL: Operator(ge, Type.COMPARISON),
    GREAT: Operator(gt, Type.COMPARISON),
}

def exec_operation(x: str, y: str, operation=MULTIPLE) -> str:
    """Executes the operation and returns the result.

    Args:
        x (str): String representation of a number.
        y (str): String representation of a number.

    Returns:
        str:  result of calculations.

    Raises:
        ValueError: If `operation` is not found`.
    """
    if operation not in OPERATORS:
        raise ValueError('operation was not found')

    if operation == POWER and y[0] == MINUS:
        a, b = float(y[1:]), float(x)
    if operation == POWER:
        a, b = float(y), float(x)
    else:
        a, b = float(x), float(y)

    operator = OPERATORS[operation]
    result = operator.func(a, b)

    if operator.type == Type.ARITHMETIC:
        if operation == POWER and y[0] == MINUS:
            return f'{MINUS}{result}'
        return f'{PLUS}{result}' if result > 0 else str(result)

    if operator.type == Type.COMPARISON:
        return str(int(result))
