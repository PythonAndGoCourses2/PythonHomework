"""Custom library for all handled operators, constants functions"""
import math
from collections import namedtuple
import operator


CONSTANTS = {'pi': math.pi, 'e': math.e}

Operator = namedtuple("Operator", ("priority", "function"))
RIGHT_ASSOCIATIVITY = {
    '^': Operator(4, operator.pow),
    '~': Operator(5, operator.neg),
    '#': Operator(5, operator.pos)
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


def make_math_functions(math_functions):
    for func in MATH_FUNCTIONS:
        FUNCTIONS[func.__name__] = func
    return FUNCTIONS


MATH_FUNCTIONS = [getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))]
FUNCTIONS = {
    'abs': abs,
    'round': round,
    'lg': math.log10
}
FUNCTIONS.update(make_math_functions(MATH_FUNCTIONS))
FUNC_DELIMITER = ','

O_BRACKET = '('
C_BRACKET = ')'
