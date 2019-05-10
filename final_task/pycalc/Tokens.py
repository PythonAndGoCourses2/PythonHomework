import math
from collections import namedtuple

# -----------------------------------------------
CONSTANTS = {'pi': math.pi, 'e': math.e}
# -----------------------------------------------
Operator = namedtuple("Operator", ("priority", "function"))
OPERATORS = dict()
OPERATORS['+'] = Operator(2, lambda a, b: a + b)
OPERATORS['-'] = Operator(2, lambda a, b: a - b)
OPERATORS['*'] = Operator(3, lambda a, b: a * b)
OPERATORS['/'] = Operator(3, lambda a, b: a / b)
OPERATORS['//'] = Operator(3, lambda a, b: a // b)
OPERATORS['%'] = Operator(3, lambda a, b: a % b)
OPERATORS['^'] = Operator(4, lambda a, b: a ** b)
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
