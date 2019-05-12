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
    HAS_COMPARE (bool): determines whether the expression has a comparison operation.
    LIBRARY (dict): library of available operations.
"""

import argparse
import re
from collections import namedtuple
from functools import reduce
from operator import mul, truediv, floordiv, mod, add, sub, lt, le, eq, ne, ge, gt
import regexp as mre

HAS_COMPARE = False
LIBRARY = {
    'abs': abs,
    'round': round,
}

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

class Type:
    ARITHMETIC = 0
    COMPARISON = 1

Operator = namedtuple('Operator', 'func type')
OPERATORS = {
    MULTIPLE: Operator(mul, Type.ARITHMETIC),
    POWER: Operator(pow, Type.ARITHMETIC),
    TRUE_DIVISION: Operator(truediv, Type.ARITHMETIC),
    FLOOR_DIVISION: Operator(floordiv, Type.ARITHMETIC),
    MODULE: Operator(mod, Type.ARITHMETIC),
    PLUS: Operator(add, Type.ARITHMETIC),
    MINUS: Operator(sub, Type.ARITHMETIC),
    LESS: Operator(lt, Type.COMPARISON),
    LESS_OR_EQUAL: Operator(le, Type.COMPARISON),
    EQUAL: Operator(eq, Type.COMPARISON),
    NOT_EQUAL: Operator(ne, Type.COMPARISON),
    GREAT_OR_EQUAL: Operator(ge, Type.COMPARISON),
    GREAT: Operator(gt, Type.COMPARISON),
}

def exec_operation(x: str, y: str, operation=MULTIPLE) -> str:
    """Executes the operation and returns the result.

    Args:
        x (str): String representation of a number.
        y (str): String representation of a number.

    Returns:
        str:  result of calculations.

    Raises:
        ValueError: If `operation` is not found`.
    """
    if operation not in OPERATORS:
        raise ValueError('operation was not found')

    if operation == POWER and y[0] == MINUS:
        a, b = float(y[1:]), float(x)
    if operation == POWER:
        a, b = float(y), float(x)
    else:
        a, b = float(x), float(y)

    operator = OPERATORS[operation]
    result = operator.func(a, b)

    if operator.type == Type.ARITHMETIC:
        if operation == POWER and y[0] == MINUS:
            return f'{MINUS}{result}'
        return f'{PLUS}{result}' if result > 0 else str(result)

    if operator.type == Type.COMPARISON:
        return str(int(result))


def replace_constant(expr: str) -> str:
    """
    Calculates constant operations.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.finditer(mre.REGEXP_CONSTANT, expr)

    for m in results:
        name = m.group('name')

        if name[-1] == LEFT_BRACKET or re.match(mre.REGEXP_DIGIT, name):
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


def replace_fanction(expr: str) -> str:
    """
    Calculates function operations.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.finditer(mre.REGEXP_FUNCTION, expr)

    for m in results:
        func = m.group('name')
        pattern = m.group('pattern')
        args = filter(bool, m.group('args').split(','))
        args = [float(v) for v in args]
        answer = str(LIBRARY[func](*args))
        expr = expr.replace(pattern, answer)

    return expr


def replace_unary_operator(expr: str) -> str:
    """
    Calculates unary operations.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.findall(mre.REGEXP_UNARY, expr)
    results.sort(key=len, reverse=True)

    for m in results:
        answer = MINUS if m.count(MINUS) % 2 else PLUS
        expr = expr.replace(m, answer)

    return expr


def replace_compare_operator(expr: str, *operations: list) -> str:
    """
    Calculates compare operations.

    Args:
        expr (str): String mathematical expression.
        *operations (list): List of operations that need to be done on the expression.

    Returns:
        str: Updated expression.
    """
    if re.search(mre.REGEXP_COMPARE, expr):
        return replace_bynary_operator(expr, *operations)

    return expr


def replace_bynary_operator(expr: str, *operations: list) -> str:
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
            delimeter = mre.REGEXP_SCREENING.format(operation=o)

        regexp = mre.REGEXP_BYNARY.format(operation=delimeter)
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


def replace_brackets(expr: str) -> str:
    """
    Calculates the expression in brackets.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: Updated expression.
    """
    results = re.findall(mre.REGEXP_BACKETS, expr)

    for m in results:
        answer = calc(m[1:-1])
        expr = expr.replace(m, answer)

    return expr


def calc(expr: str) -> str:
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

    pattern = re.compile(mre.REGEXP_SIMPLE_DIGIT)
    while True:
        for inst in OPERATION_PRIORITY:
            expr = inst.func(expr, *inst.args)
            if pattern.match(expr):
                return expr

    return expr


def import_modules(*modules: list):
    """Imports the modules from the list to the global field LIBRARY."""
    for module in modules:
        LIBRARY.update(__import__(module).__dict__)


def check_spaces(expr: str) -> str:
    """
    Checks if an expression has the wrong elements.

    Args:
        expr (str): String mathematical expression.

    Returns:
        str: cleared expression from spaces.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    res = re.findall(mre.REGEXP_INCORECT_EXPRETION, expr)
    if res:
        raise ValueError('expression is not correct')

    return expr.replace(' ', '')


def check_brackets(expr: str):
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


def check_constant(expr: str):
    """
    Checks if all constants in the expression are available.

    Args:
        expr (str): String mathematical expression.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    results = re.finditer(mre.REGEXP_CONSTANT, expr)
    for m in results:
        name = m.group('name')

        if name[-1] == LEFT_BRACKET or re.match(mre.REGEXP_DIGIT, name):
            continue

        if name[0].isdigit():
            raise ValueError(f'constant {name} can not start with digit')

        if name not in LIBRARY or callable(LIBRARY[name]):
            raise ValueError(f'there is no such constant {name}')


def check_function(expr: str):
    """
    Checks if all functions in the expression are available.

    Args:
        expr (str): String mathematical expression.

    Raises:
        ValueError: If `expr` is not correct`.
    """
    results = re.finditer(mre.REGEXP_FUNCTION, expr)
    for m in results:
        name = m.group('name')
        pattern = m.group('pattern')

        if name[0].isdigit():
            raise ValueError(f'function {pattern} can not start with digit')

        if name not in LIBRARY or not callable(LIBRARY[name]):
            raise ValueError(f'there is no such function {pattern}')


def check_expression(expr: str) -> str:
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
    HAS_COMPARE = True if re.search(mre.REGEXP_COMPARATOR, expr) else False

    return expr


def parse_query():
    """
    Convert argument strings to objects and assign them as attributes of the namespace.

    Returns:
        Namespace: got data from command line.
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


def print_answer(string: str):
    """
    Converts the resulting string to the desired type and prints it.

    Args:
        string (str): String representation of a number.
    """
    num = float(string)
    match = re.search(mre.REGEXP_NON_ZERO_FRACTION_PART, string)
    num = num if match else int(num)

    answer = bool(num) if HAS_COMPARE else num
    print(answer)


def main():
    """Performs processing and calculation of the request from the command line and displays it on the screen."""
    try:
        args = parse_query()
        import_modules('math', *args.modules)
        expr = check_expression(args.expr)
        answer = calc(expr)
        print_answer(answer)
    except Exception as e:
        print(f'ERROR: {e}')


if __name__ == '__main__':
    main()
