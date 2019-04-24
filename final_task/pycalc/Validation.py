from argparse import ArgumentParser
from . import pycalc


def parse_command_line():
    parser = ArgumentParser(description='Pure-python command-line calculator')
    parser.add_argument('EXPRESSION', type=str, help='expression string to evaluate')
    return parser.parse_args().EXPRESSION


def is_error_spaces(expression):
    new_expression = expression[0]
    for item in expression[1:]:
        if item != ' ' or new_expression[-1] != ' ':
            new_expression += item
    for i in range(1, len(new_expression)-1):
        if new_expression[i] == ' ':
            if new_expression[i-1].isalpha():
                return True
            elif new_expression[i-1].isdigit() and new_expression[i+1].isalnum():
                return True
    return False


def del_spaces(expression):
    new_expression = ''
    for i in expression:
        if i != ' ':
            new_expression += i
    return new_expression


def is_error_brackets(expression):
    opening_brackets = 0
    closing_brackets = 0
    for i, item in enumerate(expression):
        if item == '(':
            opening_brackets += 1
            if not i and expression[i - 1].isdigit():
                return True
        elif item == ')':
            closing_brackets += 1
            if closing_brackets > opening_brackets or i != len(expression)-1 and expression[i+1].isdigit():
                return True
    if opening_brackets == closing_brackets:
        return False
    return True


def is_error_symbol(expression):
    if (expression[0] in pycalc.OPERATION_PRIORITIES and expression[0] != '(') or\
            (expression[-1] in pycalc.OPERATION_PRIORITIES and expression[-1] != ')'):
        return True
    i = 0
    while i < len(expression)-1:
        if (expression[i] in pycalc.OPERATION_PRIORITIES.keys() or expression[i] == '=' or expression[i] == '!') and\
                expression[i] != ')':
            if (expression[i+1] in pycalc.OPERATION_PRIORITIES.keys() or expression[i + 1] == '=') and\
                    expression[i + 1] != '(':
                if expression[i]+expression[i+1] in pycalc.OPERATION_PRIORITIES:
                    i += 2
                    continue
                else:
                    return True
        i += 1
    return False


def check_exception():
    expression = parse_command_line()
    if expression is None or not expression.rstrip():
        print('ERROR: expression argument is required')
    elif is_error_spaces(expression):
        print('ERROR: spaces')
    else:
        expression = del_spaces(expression)
        if is_error_brackets(expression):
            print('ERROR: brackets')
        elif is_error_symbol(expression):
            print('ERROR: operator')
        else:
            return expression




