import re
import operator
import pycalc

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
    second_argument = expr[expr.rfind(item) + 1:]
    x, y = pycalc.calculating(first_argument), calculating(second_argument)
    return COMPARISON_OPERATORS[item](x, y)


def fix_unary(expr):
    """Replace unary operations"""
    if expr[0] == '-':
        expr = "0" + expr
    elif expr[0] == '+':
        expr = "0" + expr
    expr = re.sub(r'\(\-', '(0-', expr)
    expr = re.sub(r'\(\+', '(0+', expr)
    return expr


def replace_plus_minus(expr):
    while True:
        if expr.find('++') != -1:
            expr = expr.replace("++", "+")
        elif expr.find('--') != -1:
            expr = expr.replace("--", "-")
        elif expr.find('+-') != -1 or expr.find('-+') != -1:
            expr = expr.replace("+-", "-")
            expr = expr.replace("-+", "-")
        else:
            break
    return expr


def correct_check(expr):
    for operation in pycalc.OPERATORS:
        if expr.endswith(operation):
            return False
    return True
