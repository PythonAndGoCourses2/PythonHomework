import math


PRIORITY = {'<': 1, '<=': 1, '==': 1, '!=': 1, '>=': 2, '>': 1,
            '+': 2, '-': 2, '*': 3, '/': 3, '//': 3, '%': 3, '^': 4}

MATH_OPERATION = []
for i in dir(math):
    if '_' not in i:
        MATH_OPERATION.append(i)

for operation in MATH_OPERATION:
    PRIORITY[operation] = 2


def shunting_yard(parsed_formula):
    stack = []
    polish_notation = []

    for token in parsed_formula:
        if token in PRIORITY:
            while stack and stack[-1] != '(' and PRIORITY[token] <= PRIORITY[stack[-1]]:
                polish_notation.append(stack.pop())
            stack.append(token)
        elif token == ')':
            while stack:
                x = stack.pop()
                if x == '(':
                    break
                polish_notation.append(x)
        elif token == '(':
            stack.append(token)
        else:
            polish_notation.append(token)
    while stack:
        polish_notation.append(stack.pop())

    return polish_notation
