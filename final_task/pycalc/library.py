"""Custom library for all handled operators, constants functions"""
import math
from collections import namedtuple
import operator

CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'tau': math.tau
}

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


def make_math_functions():
    """Make dictionary name : func from math_functions"""
    functions = dict()
    for func in MATH_FUNCTIONS:
        functions[func.__name__] = func
    return functions


MATH_FUNCTIONS = [getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))]
OTHER_FUNCTIONS = {
    'abs': abs,
    'round': round,
    'lg': math.log10,
    'lgTwo': math.log2,
    'logOneP': math.log1p
}
FUNCTIONS = {**make_math_functions(), **OTHER_FUNCTIONS}
FUNC_DELIMITER = ','

OPEN_BRACKET = '('
CLOSE_BRACKET = ')'
NOT_SUPPORTED = '[]{}'

FILLER = 'no args'  # Constant to fill no ars functions
