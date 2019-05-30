import math
import operator
import string


numbers = string.digits
letters = string.ascii_letters
pointing = '/'
dot = '.'
comparison = '><=!'
data_set = [numbers + letters + dot, pointing, comparison]

whitespace = string.whitespace

postfix_func = ['!']
binary_operators = ['+', '-', '*', '/', '//', '%', '^', '==', '>', '<', '<=', '>=', '!=', '&', 'is', 'is not', '<<',
                    '@', '>>']

math_functions_dict = {attr: getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))}
math_functions_dict['abs'] = abs
math_functions_dict['round'] = round
math_constants_dict = {attr: getattr(math, attr) for attr in dir(math) if not callable(getattr(math, attr))}
prefix_func = list(math_functions_dict.keys())
constants = list(math_constants_dict.keys())

sep = ','


def operator_plus(*args):
    param_count = len(args)
    assert 0 < param_count < 3,  "operator_plus got more than 2 parameters"
    if param_count == 1:
        return args[0]
    return args[0] + args[1]


def operator_minus(*args):
    param_count = len(args)
    assert 0 < param_count < 3,  "operator_minus got more than 2 parameters"
    if param_count == 1:
        return -args[0]
    return args[0] - args[1]


ops_ex = {
    '+': operator_plus,
    '-': operator_minus
}

ops = {
    '+': [operator.add, 2],
    '-': [operator.sub, 2],
    '*': [operator.mul, 2],
    '/': [operator.truediv, 2],
    '//': [operator.floordiv, 2],
    '%': [operator.mod, 2],
    '^': [operator.pow, 2],

    '<': [operator.lt, 2],
    '<=': [operator.le, 2],
    '==': [operator.eq, 2],
    '!=': [operator.ne, 2],
    '>=': [operator.ge, 2],
    '>': [operator.gt, 2],

    '&': [operator.and_, 2],

    'is': [operator.is_, 2],
    'is not': [operator.is_not, 2],
    '<<': [operator.lshift, 2],
    '@': [operator.matmul, 2],
    '>>': [operator.rshift, 2],
    'not': [operator.not_, 1],
    '~': [operator.invert, 1],
}

operators_priority = {
    '^': 100,
    '~': 90,
    '*': 80,
    '/': 80,
    '%': 80,
    '//': 80,
    '+': 70,
    '-': 70,
    '>>': 60,
    '<<': 60,
    '&': 50,
    '|': 40,
    '<=': 30,
    '<': 30,
    '>=': 30,
    '>': 30,
    '<>': 25,
    '==': 25,
    '!=': 25,
    '=': 20,
    '%=': 20,
    '/=': 20,
    '-/=': 20,
    '+/=': 20,
    '*/=': 20,
    '^/=': 20,
    '**/=': 20,
    'is': 15,
    'is not': 15,
    'in': 15,
    'not in': 15,
    'not': 10,
    'and': 10,
    '(': 1,
    ')': 1
}
