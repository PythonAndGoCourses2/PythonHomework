import math


PRIORITY = {'<': 1, '<=': 1, '==': 1, '!=': 1, '>=': 2, '>': 1,
            '+': 2, '-': 2, '*': 3, '/': 3, '//': 3, '%': 3, '^': 4,
            'neg': 5, 'pos': 5}

math_functions = dir(math)


def create_polish_notation(parsed_formula):
    stack_operation = []
    stack_function = []
    polish_notation = []

    for token in parsed_formula:
        if token in PRIORITY:
            while stack_operation and stack_operation[-1] != '(' and PRIORITY[token] <= PRIORITY[stack_operation[-1]]:
                polish_notation.append(stack_operation.pop())
            stack_operation.append(token)
        elif token == ')':
            while stack_operation:
                x = stack_operation.pop()
                if x == '(':
                    break
                polish_notation.append(x)
        elif token == '(':
            stack_operation.append(token)
        elif token in math_functions:
            stack_function.append(token)
        elif token == '[':
            continue
        elif token == ']':
            while stack_operation:
                polish_notation.append(stack_operation.pop())
            polish_notation.append(stack_function.pop())
        else:
            polish_notation.append(token)
    while stack_operation:
        polish_notation.append(stack_operation.pop())

    return polish_notation
