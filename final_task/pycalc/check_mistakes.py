from pycalc.main import Stack
from pycalc.consts import *


def check_mistakes(expression, functions):

    def is_number(part):
        for char in part:
            if not char.isnumeric() and char != '.':
                return False
        return True

    if len(expression) == 0:
        return "ERROR: empty expression!"

    brackets_stack = Stack.Stack()
    for element in expression:
        if element == '(':
            brackets_stack.push('(')
        elif element == ')':
            if brackets_stack.is_empty():
                return "ERROR: brackets are not paired"

            brackets_stack.pop()
        elif element == " ":
            expression.remove(element)
    if not brackets_stack.is_empty():
        return "ERROR: brackets are not paired"

    if expression[len(expression) - 1] in signs:
        return "ERROR: no number after operator"

    main_sign_count = 0
    l_sign_count = 0
    number_count = 0
    logical_sign_pos = 0

    for index in range(len(expression)):

        if expression[index] in ['+', '-']:
            main_sign_count += 1

        elif expression[index] in ['*', '/', '^', '%', '//']:
            if number_count == 0:
                return "ERROR: no numbers before sign"

            if index != len(expression) - 1 and expression[index + 1] in ['*', '/', '^', '%', '//']:
                return "ERROR: duplicate multiply or div sign"

        elif expression[index] in logical_signs:
            l_sign_count += 1
            logical_sign_pos = index
            if l_sign_count > 1:
                return "ERROR: more than one logical operator"

        elif expression[index] == '=':
            return "ERROR: illegal usage '='"

        elif is_number(expression[index]):
            number_count += 1
            if index != len(expression) - 1 and is_number(expression[index + 1]):
                return "ERROR: no sign between expression"

        elif expression[index].isalpha():
            if expression[index] in math_consts:
                number_count += 1
            elif expression[index] in functions:
                if index == len(expression) - 1 or expression[index + 1] != '(':
                    return "ERROR: no brackets after function"

            else:
                return "ERROR: function does not exist"

    if l_sign_count == 1:
        if (len(expression[:logical_sign_pos])) == 0 or (len(expression[logical_sign_pos:])) == 0 \
                or logical_sign_pos in [0, len(expression) - 1]:
            return "ERROR: one of expressions around logical operator is empty"

    if number_count == 0:
        return "ERROR: no numbers in expression"

    return ''
