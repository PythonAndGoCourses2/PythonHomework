"""Custom library for all handled operators, constants functions"""
import importlib
import math
import operator
from collections import namedtuple


def make_functions(math_functions):
    """Make dictionary name : func from math_functions"""
    functions = dict()
    for func in math_functions:
        functions[func.__name__] = func
    return functions


class Library:
    CONSTANTS = {
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau
    }
    user_constants = dict()

    Operator = namedtuple("Operator", ("priority", "function"))
    UNARY_MINUS = '~'
    UNARY_PLUS = '#'
    RIGHT_ASSOCIATIVITY = {
        '^': Operator(4, operator.pow),
        UNARY_MINUS: Operator(5, operator.neg),
        UNARY_PLUS: Operator(5, operator.pos)
    }
    LEFT_ASSOCIATIVITY = {
        '>': Operator(1, operator.gt),
        '>=': Operator(1, operator.ge),
        '<': Operator(1, operator.lt),
        '<=': Operator(1, operator.le),
        '==': Operator(1, operator.eq),
        '!=': Operator(1, operator.ne),
        '+': Operator(2, operator.add),
        '-': Operator(2, operator.sub),
        '*': Operator(3, operator.mul),
        '/': Operator(3, operator.truediv),
        '//': Operator(3, operator.floordiv),
        '%': Operator(3, operator.mod),
    }
    OPERATORS = {**LEFT_ASSOCIATIVITY, **RIGHT_ASSOCIATIVITY}

    MATH_FUNCTIONS = [getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))]
    OTHER_FUNCTIONS = {
        'abs': abs,
        'round': round,
        'lg': math.log10,
        'lgTwo': math.log2,
        'logOneP': math.log1p
    }
    user_functions = dict()
    FUNCTIONS = {**make_functions(MATH_FUNCTIONS), **OTHER_FUNCTIONS}
    FUNC_DELIMITER = ','

    OPEN_BRACKET = '('
    CLOSE_BRACKET = ')'

    def read_user_module(self, module_name):
        """'Read' user module: make functions and constants"""
        module = importlib.import_module(module_name)
        functions = [getattr(module, attr)
                     for attr in dir(module) if callable(getattr(module, attr))]
        constants = {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
                     and not callable(getattr(module, k))}
        Library.user_functions = {**make_functions(functions)}
        Library.user_constants = constants
