"""This module checks the correctness of the entered expression."""

import re
import core
from constants import *
from core import comma_count


def brackets_check(expr):
    """Check brackets balance"""
    if expr.count('(') != expr.count(')'):
        print("ERROR: brackets are not balanced")
        return False
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
    """Replace unary operations.For example:
    -1+2 -> 0-1+2
    1*-2 -> 1*(0-2)
    1*(-2) -> 1*(0-2)
    """
    regexp = re.compile(r"(?P<op>(\*|\/|\^))"
                        r"(?P<operation>(\+|-))"
                        r"(?P<digits>([\d\.]+))"
                        )
    search_result = regexp.finditer(expr)
    for item in search_result:
        temp = item.group("operation") + item.group("digits")
        expr = re.sub(temp, "(0" + temp + ")", expr)
    if expr.startswith("-") or expr.startswith("+"):
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


def replace_whitespace_and_const(expr):
    expr = expr.replace(" ", "")
    for constant in MATH_CONST.keys():
        expr = expr.replace(constant, str(MATH_CONST[constant]))
    return expr


def common_check(expr):
    # regexp = re.compile(r"(?P<function>[-a-zA-Z]+)")
    # search_function = regexp.finditer(expr)
    # for item in search_function:
    #     func = item.group("function")
    #     if func not in MATH_FUNC and func not in MATH_CONST:
    #         print("Unknowm function '{}'".format(func))
    #         return False
    for operation in OPERATORS:  # Если последний символ строки операция
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


def check_arg_function(expr):
    print("expr= ", expr)
    func = ""
    count, count_comma, i = 0, 0, 0
    while i < len(expr):
        if expr[i].isalpha():
            func += expr[i]
        elif func in MATH_FUNC:
            while expr[i] != "(":  # For such function as log2, log10, etc
                func += expr[i]
                i += 1
            i += 1
            count += comma_count(MATH_FUNC[func])
            func = ""
        i += 1
    for symbol in expr:
        if symbol == ',':
            count_comma += 1
    if count != count_comma:
        return False
    return expr
