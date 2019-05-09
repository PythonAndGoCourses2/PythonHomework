import math
from collections import namedtuple

# math_functions = [getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))]
# maths = dict()
# for func in math_functions:
#     maths[func.__name__] = func


# -----------------------------------------------
CONSTANTS = {'pi': math.pi, 'e': math.e}
# -----------------------------------------------
Operator = namedtuple("Operator", ("priority", "function"))
OPERATORS = {}
OPERATORS['+'] = Operator(2, lambda a, b: a + b)
OPERATORS['-'] = Operator(2, lambda a, b: a - b)
OPERATORS['*'] = Operator(3, lambda a, b: a * b)
OPERATORS['/'] = Operator(3, lambda a, b: a / b)


# -----------------------------------------------


def get_postfix(input_string):
    output_string = []
    stack = [0]
    for token in input_string:
        if is_number(token):
            output_string.append(token)
            continue
        if token in CONSTANTS:
            output_string.append(CONSTANTS[token])
            continue
        if token in OPERATORS:
            while (stack[-1] in OPERATORS) and (OPERATORS[token].priority <= OPERATORS[stack[-1]].priority):
                output_string += stack.pop()
            else:
                stack.append(token)
    while stack[-1] in OPERATORS:
        output_string += stack.pop()
    return output_string


def is_number(s):
    return s.isdigit()
