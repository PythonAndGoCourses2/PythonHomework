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


# ------------------------------------------------


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
        if token in FUNCTIONS:
            stack.append(token)
        if token == func_delimiter:
            while not stack[-1] == openBracket:
                output_string += stack.pop()
                if not stack:
                    print('ERROR: miss delimiter or open bracket')
                    break
            continue
        if token in OPERATORS:
            while (stack[-1] in OPERATORS) and (OPERATORS[token].priority <= OPERATORS[stack[-1]].priority):
                output_string += stack.pop()
            else:
                stack.append(token)
            continue
        if token == openBracket:
            stack.append(token)
            continue
        if token == closeBracket:
            while not stack[-1] == openBracket:
                output_string += stack.pop()
                if not stack:
                    print('ERROR: miss bracket')
                    break
            stack.pop()
            if stack[-1] in FUNCTIONS:
                output_string += stack.pop()
            continue
    while stack[-1] in OPERATORS:
        output_string += stack.pop()
    return output_string


def is_number(s):
    return s.isdigit()
