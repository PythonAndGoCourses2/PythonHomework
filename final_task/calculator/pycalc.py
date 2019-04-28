# -*- coding: utf-8 -*-
"""
The module is designed to work with mathematical expressions.

Example:
        $ python pycalc.py -h
        $ python pycalc.py 'expretion'
        $ python pycalc.py 'expretion' -m 'module1' 'module2'

Attributes:
    LEFT_BRACKET (str): possible representation of the bracket ( in the expression.
    RIGHT_BRACKET (str): possible representation of the bracket ) in the expression.
    MULTIPLE (str): possible representation of the operation * in the expression.
    POWER (str): possible representation of the operation ** in the expression.
    TRUE_DIVISION (str): possible representation of the operation / in the expression.
    FLOOR_DIVISION (str): possible representation of the operation // in the expression.
    MODULE (str): possible representation of the operation % in the expression.
    PLUS (str): possible representation of the operation + in the expression.
    MINUS (str): possible representation of the operation - in the expression.
    LESS (str): possible representation of the operation < in the expression.
    LESS_OR_EQUAL (str): possible representation of the operation <= in the expression.
    GREAT (str): possible representation of the operation > in the expression.
    GREAT_OR_EQUAL (str): possible representation of the operation >= in the expression.
    EQUAL (str): possible representation of the operation == in the expression.
    NOT_EQUAL (str): possible representation of the operation != in the expression.
    REGEXP_DIGIT (rstr): regular expressions for finding numbers.
    REGEXP_SIMPLE_DIGIT (rstr): regular expressions for checking common digits.
    REGEXP_SCREENING (rstr): regular expressions for operation screening.
    REGEX_NAME (rstr): regular expressions for finding names.
    REGEXP_BACKETS (rstr): regular expressions for finding brackets.
    REGEXP_FUNCTION (rstr): regular expressions for finding functons.
    REGEXP_CONSTANT (rstr): regular expressions for finding constant names.
    REGEXP_UNARY (rstr): regular expressions for finding unary operation.
    REGEXP_BYNARY (rstr): regular expressions for finding bynary operation.
    REGEXP_COMPARE (rstr): regular expressions for finding compare operation.
    REGEXP_INCORECT_EXPRETION (rstr): regular expressions for defining invalid expressions.
    REGEXP_NON_ZERO_FRACTION_PART (rstr): regular expressions for finding non-zero fraction part.
    REGEXP_COMPARATOR (rstr): regular expressions for finding comparator.
    HAS_COMPARE (bool): determines whether the expression has a comparison operation.
    LIBRARY (dict): library of available operations.
"""

import argparse
import re
from collections import namedtuple
from functools import reduce
from operator import mul, truediv, floordiv, mod, add, sub, lt, le, eq, ne, ge, gt

LEFT_BRACKET = '('
RIGHT_BRACKET = ')'
MULTIPLE = '*'
POWER = '^'
TRUE_DIVISION = '/'
FLOOR_DIVISION = '//'
MODULE = '%'
PLUS = '+'
MINUS = '-'
LESS = '<'
LESS_OR_EQUAL = '<='
GREAT = '>'
GREAT_OR_EQUAL = '>='
EQUAL = '=='
NOT_EQUAL = '!='

REGEXP_DIGIT = r'[+-]?\d+\.\d+e\+\d+|[+-]?\d+\.?\d*|[+-]?\d*\.?\d+'
REGEXP_SIMPLE_DIGIT = rf'^({REGEXP_DIGIT})$'
REGEXP_SCREENING = rf'\{{operation}}'
REGEX_NAME = r'\w+'
REGEXP_BACKETS = r'(?:^|\W)(\([^)(]+\))'
REGEXP_FUNCTION = rf'(?P<pattern>(?P<name>{REGEX_NAME})\((?P<args>(?:{REGEXP_DIGIT})(?:,(?:{REGEXP_DIGIT})+)*|)\))'
REGEXP_CONSTANT = rf'(?P<name>{REGEXP_DIGIT}|{REGEX_NAME}\(?)'
REGEXP_UNARY = rf'([-+]{{2,}})'
REGEXP_BYNARY = rf'((?:{REGEXP_DIGIT})(?:{{operation}}(?:{REGEXP_DIGIT}))+)'
REGEXP_COMPARE = rf'^{REGEXP_BYNARY}$'.format(operation='[=!<>]{1,2}')
REGEXP_NON_ZERO_FRACTION_PART = r'\.0*[1-9]'
REGEXP_COMPARATOR = r'[=!<>]{1,2}'
REGEXP_INCORECT_EXPRETION = (
    r'.?\W\d+\s*\(|'
    r'^\d+\s*\(|'
    r'^\W*$|'
    r'\d+[)(<=!>][<>!]\d+|'
    r'\W\d+[)(<=!>][<!>]\d+|'
    r'\w+\s+\w+|'
    r'[-+*^\/%<=!>]+\s+[\/*^%<=!>]+|'
    r'^[\/*^%<=!>]|'
    r'[-+*^\/%<=!>]$'
)

HAS_COMPARE = False
LIBRARY = {
    'abs': abs,
    'round': round,
}


def exec_operation(x, y, operation=MULTIPLE):
    """Executes the operation and returns the result.

    Args:
        x (str): String representation of a number.
        y (str): String representation of a number.

    Returns:
        str:  result of calculations.

    Raises:
        ValueError: If `operation` is not found`.
    """
    if operation == POWER and y[0] == MINUS:
        a, b = float(y[1:]), float(x)
    if operation == POWER:
        a, b = float(y), float(x)
    else:
        a, b = float(x), float(y)

    result = None
    # arithmetic operation
    if operation == MULTIPLE:
        result = mul(a, b)
    elif operation == POWER:
        result = pow(a, b)
    elif operation == TRUE_DIVISION:
        result = truediv(a, b)
    elif operation == FLOOR_DIVISION:
        result = floordiv(a, b)
    elif operation == MODULE:
        result = mod(a, b)
    elif operation == PLUS:
        result = add(a, b)
    elif operation == MINUS:
        result = sub(a, b)

    if operation == POWER and y[0] == MINUS:
        return f'{MINUS}{result}'
    if result is not None:
        return f'{PLUS}{result}' if result > 0 else str(result)

    # comparison operation
    if operation == LESS:
        result = lt(a, b)
    elif operation == LESS_OR_EQUAL:
        result = le(a, b)
    elif operation == EQUAL:
        result = eq(a, b)
    elif operation == NOT_EQUAL:
        result = ne(a, b)
    elif operation == GREAT_OR_EQUAL:
        result = ge(a, b)
    elif operation == GREAT:
        result = gt(a, b)

    if result is not None:
        return str(int(result))

    raise ValueError('operation was not found')


def replace_constant(expr):
    """
    Calculates constant operations.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.finditer(REGEXP_CONSTANT, expr)

    for m in results:
        name = m.group('name')

        if name[-1] == LEFT_BRACKET or re.match(REGEXP_DIGIT, name):
            continue

        answer = str(LIBRARY[name])
        arr = expr.split(name)

        for idx, piece in enumerate(arr[:-1]):
            if piece and piece[-1].isalnum():
                arr[idx] = f'{piece}{name}'
            elif piece or not idx:
                arr[idx] = f'{piece}{answer}'

        expr = ''.join(arr)

    return expr


def replace_fanction(expr):
    """
    Calculates function operations.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.finditer(REGEXP_FUNCTION, expr)

    for m in results:
        func = m.group('name')
        pattern = m.group('pattern')
        args = filter(bool, m.group('args').split(','))
        args = [float(v) for v in args]
        answer = str(LIBRARY[func](*args))
        expr = expr.replace(pattern, answer)

    return expr


def replace_unary_operator(expr):
    """
    Calculates unary operations.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.findall(REGEXP_UNARY, expr)
    results.sort(key=len, reverse=True)

    for m in results:
        answer = MINUS if m.count(MINUS) % 2 else PLUS
        expr = expr.replace(m, answer)

    return expr


def replace_compare_operator(expr, *operations):
    """
    Calculates compare operations.

    Args:
        expr (str): String mathematical expression.
        *operations (list): List of operations that need to be done on the expression.

    Returns:
        str: Updated expression.
    """
    if re.search(REGEXP_COMPARE, expr):
        return replace_bynary_operator(expr, *operations)

    return expr


def replace_bynary_operator(expr, *operations):
    """
    Calculates binary operations.

    Args:
        expr (str): String mathematical expression.
        *operations (list): List of operations that need to be done on the expression.

    Returns:
        str: Updated expression.
    """
    for o in operations:
        delimeter = o
        if o == PLUS or o == MULTIPLE or o == POWER:
            delimeter = REGEXP_SCREENING.format(operation=o)

        regexp = REGEXP_BYNARY.format(operation=delimeter)
        results = re.findall(regexp, expr)
        for m in results:
            arr = list(filter(bool, m.split(o)))
            if o == MINUS and m[0] == MINUS:
                arr[0] = f'{MINUS}{arr[0]}'
            if o == POWER:
                arr = arr[::-1]

            answer = reduce(lambda a, b: exec_operation(a, b, operation=o), arr)
            expr = expr.replace(m, answer)

    return expr


def replace_brackets(expr):
    """
    Calculates the expression in brackets.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.findall(REGEXP_BACKETS, expr)

    for m in results:
        answer = calc(m[1:-1])
        expr = expr.replace(m, answer)

    return expr


def calc(expr):
    """
    Calculates the result from the getting expression.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: result of calculations.
    """
    Operation = namedtuple('Operation', 'func args')
    OPERATION_PRIORITY = [
        Operation(replace_constant, []),
        Operation(replace_fanction, []),
        Operation(replace_brackets, []),
        Operation(replace_unary_operator, []),
        Operation(replace_bynary_operator, [POWER]),
        Operation(replace_bynary_operator, [MULTIPLE, TRUE_DIVISION, FLOOR_DIVISION, MODULE]),
        Operation(replace_bynary_operator, [PLUS, MINUS]),
        Operation(replace_compare_operator, [EQUAL, NOT_EQUAL, GREAT, GREAT_OR_EQUAL, LESS, LESS_OR_EQUAL]),
    ]

    pattern = re.compile(REGEXP_SIMPLE_DIGIT)
    while True:
        for inst in OPERATION_PRIORITY:
            expr = inst.func(expr, *inst.args)
            if pattern.match(expr):
                return expr

    return expr


def import_modules(*modules):
    """Imports the modules from the list to the global field LIBRARY."""
    for module in modules:
        LIBRARY.update(__import__(module).__dict__)


def check_spaces(expr):
    """
    Checks if an expression has the wrong elements.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: cleared expression from spaces.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    res = re.findall(REGEXP_INCORECT_EXPRETION, expr)
    if res:
        raise ValueError('expression is not correct')

    return expr.replace(' ', '')


def check_brackets(expr):
    """
    Checks if all brackets have a pair.

    Args:
        expr (str): String mathematical expression.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    stack = []
    for c in expr:
        if c == LEFT_BRACKET:
            stack.append(c)
        elif c == RIGHT_BRACKET and (not stack or stack.pop() != LEFT_BRACKET):
            raise ValueError('brackets are not balanced')

    if stack:
        raise ValueError('brackets are not balanced')


def check_constant(expr):
    """
    Checks if all constants in the expression are available.

    Args:
        expr (str): String mathematical expression.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    results = re.finditer(REGEXP_CONSTANT, expr)

    for m in results:
        name = m.group('name')

        if name[-1] == LEFT_BRACKET or re.match(REGEXP_DIGIT, name):
            continue

        if name[0].isdigit():
            raise ValueError(f'constant {name} can not start with digit')

        if name not in LIBRARY or callable(LIBRARY[name]):
            raise ValueError(f'there is no such constant {name}')


def check_function(expr):
    """
    Checks if all functions in the expression are available.

    Args:
        expr (str): String mathematical expression.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    results = re.finditer(REGEXP_FUNCTION, expr)
    for m in results:
        name = m.group('name')
        pattern = m.group('pattern')

        if name[0].isdigit():
            raise ValueError(f'function {pattern} can not start with digit')

        if name not in LIBRARY or not callable(LIBRARY[name]):
            raise ValueError(f'there is no such function {pattern}')


def check_expression(expr):
    """
    Checks the expression for correctness.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: cleared expression.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    expr = check_spaces(expr)
    check_brackets(expr)
    check_constant(expr)
    check_function(expr)

    global HAS_COMPARE
    HAS_COMPARE = True if re.search(REGEXP_COMPARATOR, expr) else False

    return expr


def parse_query():
    """
    Convert argument strings to objects and assign them as attributes of the namespace.

    Returns:
        Namespace: If there is no fractional part.
    """
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('expr', metavar='EXPRESSION', help='expression string to evaluate')
    parser.add_argument('-m',
                        '--use-modules',
                        default=[],
                        dest='modules',
                        metavar='MODULE',
                        nargs='+',
                        help='additional modules to use')

    return parser.parse_args()


def convert_answer(string):
    """
    Converts the resulting string to the desired type.

    Args:
        string (str): String representation of a number.

    Returns:
        int: If there is no fractional part.
        float: If there is a fractional part.
        bool: If the expression contained some equality.
    """
    num = float(string)
    match = re.search(REGEXP_NON_ZERO_FRACTION_PART, string)
    num = num if match else int(num)

    return bool(num) if HAS_COMPARE else num


def main():
    """Performs processing and calculation of the request from the command line and displays it on the screen."""
    try:
        args = parse_query()
        import_modules('math', *args.modules)
        expr = check_expression(args.expr)
        answer = calc(expr)
        answer = convert_answer(answer)
        print(answer)
    except Exception as e:
        print(f'ERROR: {e}')


if __name__ == '__main__':
    main()
