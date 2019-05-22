"""Operators manager module"""

import math
import operator


def create_func_dict():
    """
    Returns dictionary where keys are the name of functions and constants from module math,
    and values are a dictionary {'operator': <built-in-function>, 'priority': number}

    """
    func_dict = {
                'abs': {'operator': abs, 'priority': 0},
                'round': {'operator': round, 'priority': 0}
                }
    for key, value in math.__dict__.items():
        if key.startswith('_'):
            continue
        func_dict[key] = {'operator': value, 'priority': 0}
    return func_dict


function_dict = create_func_dict()

operator_dict = {
    '+': {'operator': operator.add, 'priority': 4},
    '-': {'operator': operator.sub, 'priority': 4},
    '/': {'operator': operator.truediv, 'priority': 3},
    '*': {'operator': operator.mul, 'priority': 3},
    '%': {'operator': operator.mod, 'priority': 3},
    '//': {'operator': operator.floordiv, 'priority': 3},
    '^': {'operator': operator.pow, 'priority': 1},
    '**': {'operator': operator.pow, 'priority': 1},
    '==': {'operator': operator.eq, 'priority': 5},
    '!=': {'operator': operator.ne, 'priority': 5},
    '>': {'operator': operator.gt, 'priority': 5},
    '<': {'operator': operator.lt, 'priority': 5},
    '>=': {'operator': operator.ge, 'priority': 5},
    '<=': {'operator': operator.le, 'priority': 5},
}

unary_dict = {
    '-': {'operator': operator.sub, 'priority': 2}
}
