"""Operators manager module"""

import math
import operator
import importlib


def create_func_dict(func_name=None):
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
    if func_name:
        for key, value in func_name.items():
            func_dict[key] = {'operator': value, 'priority': 0}
    return func_dict


def find_user_functions(module):
    """
    Create a dict of functions and constants from user module,
    if user module and pycaclc is located in the one package
    :param module: name of the user module (optional argument)
    :return: dict {function_name: function}
    """
    try:
        user_module = importlib.import_module('{}'.format(module))
        item = [i for i in dir(user_module) if not i.startswith('_')]
        user_functions = {i: user_module.__dict__[i] for i in item}
    except ImportError:
        raise SyntaxError('There is no module with name {}'.format(module))
    return user_functions


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
