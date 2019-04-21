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

lowest_priority_operator = '('
low_priority_operators = ('<', '==', '!=', '>=', '>')
mid_priority_operators = ('+', '-')
high_priority_operators = ('*', '/', '%', '//')
highest_priority_operator = '^'

LOWEST_PRIORITY = 0
LOW_PRIORITY = 1
MID_PRIORITY = 2
HIGH_PRIORITY = 3
HIGHEST_PRIORITY = 4

RE_MAIN_PARSE_ARG = re.compile(r'\d+[.]\d+|\d+|[+,\-*^]|[/=!<>]+|\w+|[()]')
#
RE_NEGATIVE_VALUES = re.compile(r'[^\w)]+[\-]\d+[.]\d+|[^\w)]+[\-]\d+')
#
RE_NEGATIVE_VALUES_ON_STR_BEG = re.compile(r'^-\d+[.]\d+|^-\w+')
#
RE_INTS = re.compile(r'\d+')
#
RE_FLOATS = re.compile(r'\d+[.]\d+')
#
RE_FUNCTIONS = re.compile(r'[a-zA-Z]+[0-9]+|[a-zA-Z]+')
#
RE_OPERATIONS = re.compile(r'[(<=!>+\-*/%^]+')
#
RE_NEGATIVE_FUNCS = re.compile(r'[^\w)]-\w+[(].+[)]')

imports = ['math']
