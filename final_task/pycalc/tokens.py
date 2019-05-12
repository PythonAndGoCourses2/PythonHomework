"""Custom library for all handled operators, constants functions"""
import math
from collections import namedtuple


CONSTANTS = {'pi': math.pi, 'e': math.e}
# -----------------------------------------------
Operator = namedtuple("Operator", ("priority", "function"))
RIGHT_ASSOCIATIVITY = dict()
LEFT_ASSOCIATIVITY = dict()
LEFT_ASSOCIATIVITY['>'] = Operator(1, lambda a, b: a > b)
LEFT_ASSOCIATIVITY['>='] = Operator(1, lambda a, b: a >= b)
LEFT_ASSOCIATIVITY['<'] = Operator(1, lambda a, b: a < b)
LEFT_ASSOCIATIVITY['<='] = Operator(1, lambda a, b: a <= b)
LEFT_ASSOCIATIVITY['=='] = Operator(1, lambda a, b: a == b)
LEFT_ASSOCIATIVITY['!='] = Operator(1, lambda a, b: a != b)
LEFT_ASSOCIATIVITY['+'] = Operator(2, lambda a, b: a + b)
LEFT_ASSOCIATIVITY['-'] = Operator(2, lambda a, b: a - b)
LEFT_ASSOCIATIVITY['*'] = Operator(3, lambda a, b: a * b)
LEFT_ASSOCIATIVITY['/'] = Operator(3, lambda a, b: a / b)
LEFT_ASSOCIATIVITY['//'] = Operator(3, lambda a, b: a // b)
LEFT_ASSOCIATIVITY['%'] = Operator(3, lambda a, b: a % b)
RIGHT_ASSOCIATIVITY['^'] = Operator(4, lambda a, b: a ** b)
OPERATORS = {**LEFT_ASSOCIATIVITY, **RIGHT_ASSOCIATIVITY}
# ------------------------------------------------
MATH_FUNCTIONS = [getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))]
FUNCTIONS = dict()
for func in MATH_FUNCTIONS:
    FUNCTIONS[func.__name__] = func
FUNCTIONS['abs'] = abs
FUNCTIONS['round'] = round
FUNCTIONS['lg'] = math.log10
FUNC_DELIMITER = ','
# -----------------------------------------------
O_BRACKET = '('
C_BRACKET = ')'
