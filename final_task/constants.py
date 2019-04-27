"""

module which contains base constant values which uses for calculating expressions

"""

import re
import operator

operator = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '^': operator.pow,
    '//': operator.floordiv,
    '==': operator.eq,
    '<=': operator.le,
    '>=': operator.ge,
    '>': operator.gt,
    '<': operator.lt,
    '!=': operator.ne
}

priority_dict = {
    '(':  0,
    '<':  1,
    '==': 1,
    '!=': 1,
    '>=': 1,
    '>':  1,
    '+':  2,
    '-':  2,
    '*':  3,
    '/':  3,
    '%':  3,
    '//': 3,
    '^':  4
}

# regular expression which divides string by funcs operators constants and numeric values
RE_MAIN_PARSE_ARG = re.compile(r'\d+[.]\d+|\d+|[+,\-*^%]|[/=!<>]+|\w+|[()]')
RE_NEGATIVE_VALUES = re.compile(r'[^\w)]+[\-]\d+[.]\d+|[^\w)]+[\-]\d+')
RE_NEGATIVE_VALUES_ON_STR_BEG = re.compile(r'^-\d+[.]\d+|^-\w+')
RE_INTS = re.compile(r'\d+')
RE_FLOATS = re.compile(r'\d+[.]\d+')
RE_FUNCTIONS = re.compile(r'[a-zA-Z]+[0-9]+|[a-zA-Z]+')
RE_OPERATIONS = re.compile(r'[(<=!>+\-*/%^]+')
RE_NEGATIVE_FUNCS = re.compile(r'[^\w)]-\w+[(].+[)]')
RE_INCOMPLETE_FLOAT = re.compile(r'[^\d][.]\d')
RE_NEGATIVE_CONSTANTS = re.compile(r'[^\w)][\-][a-zA-Z]+[0-9]+|[^\w)][\-][a-zA-Z]+')

imports = ['math']
