"""Custom library for all handled operators, constants functions"""
import sys
import os
import importlib
import math
import operator
from collections import namedtuple


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

    MATH_FUNCTIONS = {k: v for (k, v) in math.__dict__.items() if not k.startswith('_')
                      and callable(getattr(math, k))}
    OTHER_FUNCTIONS = {
        'abs': abs,
        'round': round,
        'lg': math.log10,
        'lgTwo': math.log2,
        'logOneP': math.log1p
    }
    user_functions = dict()
    FUNCTIONS = {**MATH_FUNCTIONS, **OTHER_FUNCTIONS}
    FUNC_DELIMITER = ','

    OPEN_BRACKET = '('
    CLOSE_BRACKET = ')'
    NOT_SUPPORTED = '[]{}'

    FILLER = 'no args'  # Constant to fill no ars functions

    def read_user_module(self, module_name):
        """'Read' user module: make functions and constants"""
        sys.path.insert(0, os.getcwd())
        module = importlib.import_module(module_name)
        functions = {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
                     and callable(getattr(module, k))}
        constants = {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
                     and not callable(getattr(module, k))}
        Library.user_functions.update(functions)
        Library.user_constants.update(constants)
