import operator
import math

OPERATORS = {'+': operator.add, '-': operator.sub,
             '*': operator.mul, '/': operator.truediv,
             '//': operator.floordiv, '%': operator.mod,
             '^': operator.pow, 'neg': operator.neg,
             'pos': operator.pos}

math_functions = math.__dict__


def calc(polish):
    stack = []
    for token in polish:
        if token == 'neg' or token == 'pos':
            x = stack.pop()
            stack.append(OPERATORS[token](x))
        elif token in OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(OPERATORS[token](x, y))
        elif token in math_functions:
            x = stack.pop()
            stack.append(math_functions[token](x))
        else:
            stack.append(token)
    return stack[0]