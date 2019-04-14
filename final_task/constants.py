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
low_priority_operators = ('<', '=', '==', '!=', '>=', '>')
mid_priority_operators = ('+', '-')
high_priority_operators = ('*', '/', '%', '//')
highest_priority_operator = '^'

LOWEST_PRIORITY = 0
LOW_PRIORITY = 1
MID_PRIORITY = 2
HIGH_PRIORITY = 3
HIGHEST_PRIORITY = 4

RE_INTS = re.compile(r'[0-9]+')
RE_FLOATS = re.compile(r'[0-9]+.[0-9]+')
RE_FUNCTIONS = re.compile(r'[a-zA-Z]+[0-9]+|[a-zA-Z]+')
RE_OPERATIONS = re.compile(r'[(<=!>+\-*/%^]+')

imports = ['builtins', 'math']
