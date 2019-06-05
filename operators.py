import math
from collections import namedtuple


Operator = namedtuple('Operator', ("priority", "type", "func"))
operators = {
    '+': Operator(3, 'inf', lambda a, b: a + b),
    '-': Operator(3, 'inf', lambda a, b: a - b),
    '*': Operator(2, 'inf', lambda a, b: a * b),
    '/': Operator(2, 'inf', lambda a, b: a / b),
    '//': Operator(2, 'inf', lambda a, b: a // b),
    '%': Operator(2, 'inf', lambda a, b: getattr(math, 'fmod')(a, b)),
    '^': Operator(1, 'inf', lambda a, b: getattr(math, 'pow')(a, b)),
    '<': Operator(4, 'inf', lambda a, b: a < b),
    '<=': Operator(4, 'inf', lambda a, b: a <= b),
    '==': Operator(5, 'inf', lambda a, b: a == b),
    '!=': Operator(5, 'inf', lambda a, b: a != b),
    '>=': Operator(4, 'inf', lambda a, b: a >= b),
    '>': Operator(4, 'inf', lambda a, b: a > b),
    '!': Operator(5, 'post', lambda a: getattr(math, 'factorial')(a))
    }

math_func = {'abs': abs,
             'round': round}
[math_func.update({attr: getattr(math, attr)}) for attr in dir(math) if callable(getattr(math, attr))]
parentheses = {'(': 3, ')': 3}
list_of_op = list(operators.keys()) + list(parentheses.keys())
