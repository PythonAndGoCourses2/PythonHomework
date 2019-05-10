import math
from collections import namedtuple

# -----------------------------------------------
CONSTANTS = {'pi': math.pi, 'e': math.e}
# -----------------------------------------------
Operator = namedtuple("Operator", ("priority", "function"))
right_associativity = dict()
left_associativity = dict()
left_associativity['>'] = Operator(1, lambda a, b: a > b)
left_associativity['>='] = Operator(1, lambda a, b: a >= b)
left_associativity['<'] = Operator(1, lambda a, b: a < b)
left_associativity['<='] = Operator(1, lambda a, b: a <= b)
left_associativity['=='] = Operator(1, lambda a, b: a == b)
left_associativity['!='] = Operator(1, lambda a, b: a != b)
left_associativity['+'] = Operator(2, lambda a, b: a + b)
left_associativity['-'] = Operator(2, lambda a, b: a - b)
left_associativity['*'] = Operator(3, lambda a, b: a * b)
left_associativity['/'] = Operator(3, lambda a, b: a / b)
left_associativity['//'] = Operator(3, lambda a, b: a // b)
left_associativity['%'] = Operator(3, lambda a, b: a % b)
right_associativity['^'] = Operator(4, lambda a, b: a ** b)
OPERATORS = {**left_associativity, **right_associativity}
# ------------------------------------------------
math_functions = [getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))]
FUNCTIONS = dict()
for func in math_functions:
    FUNCTIONS[func.__name__] = func
FUNCTIONS['abs'] = abs
FUNCTIONS['round'] = round
func_delimiter = ','
# -----------------------------------------------
openBracket = '('
closeBracket = ')'
