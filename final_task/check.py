"""This module checks the correctness of the entered expression."""

import re
import operator
import core

COMPARISON_OPERATORS = {'>=': operator.ge,
                        '<=': operator.le,
                        '!=': operator.ne,
                        '==': operator.eq,
                        '>': operator.gt,
                        '<': operator.lt}


def brackets_check(expr):
    """Check brackets balance"""
    brackets = 0
    for symbol in expr:
        if symbol == '(':
            brackets += 1
        elif symbol == ')':
            brackets -= 1
    if brackets != 0:
        print("ERROR: brackets are not balanced")
        return False
    else:
        return True


def comparison_check(expr):
    """return True if the operation type is a comparison"""
    for key in COMPARISON_OPERATORS.keys():
        if key in expr:
            return key
    else:
        return False


def comparison_calc(expr, item):
    first_argument = expr[:expr.find(item)]
    if item in '<>':  # For '>', '<'
        second_argument = expr[expr.rfind(item) + 1:]
    else:
        second_argument = expr[expr.rfind(item) + 2:]
    if '=' in second_argument:
        print("ERROR: incorrect expression.")
        exit(-1)
    x, y = core.calculating(first_argument), core.calculating(second_argument)
    return COMPARISON_OPERATORS[item](x, y)


def fix_unary(expr):
    """Replace unary operations"""
    if expr.startswith("-"):
        expr = "0" + expr
    elif expr.startswith("+"):
        expr = "0" + expr
    expr = re.sub(r'\(\-', '(0-', expr)
    expr = re.sub(r'\(\+', '(0+', expr)
    return expr


def replace_plus_minus(expr):
    while True:
        if expr.find('++') != -1:
            expr = expr.replace("++", "+")
        elif expr.find('--') != -1:
            expr = expr.replace("--", "+")
        elif expr.find('+-') != -1 or expr.find('-+') != -1:
            expr = expr.replace("+-", "-")
            expr = expr.replace("-+", "-")
        else:
            break
    return expr


def correct_check(expr):
    for operation in core.OPERATORS:  # Если последний символ строки операция
        if expr.endswith(operation):
            return False
    expr_list = expr.split()
    i = 0
    while i < len(expr_list) - 1:
        if expr_list[i].isdigit() and expr_list[i + 1].isdigit():
            return False
        if expr_list[i] in "/*^%" and expr_list[i + 1] in "/*^%":
            return False
        i += 1
    return expr


def replace_whitespace_and_const(expr):
    expr = expr.replace(" ", "")
    for constant in core.MATH_CONST.keys():
        expr = expr.replace(constant, str(core.MATH_CONST[constant]))
    return expr
