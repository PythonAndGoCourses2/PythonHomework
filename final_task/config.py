import math
import operator


minus_plus_characters = {
    '++': '+',
    '+-': '-',
    '-+': '-',
    '--': '+'
}

brackets = '(', ')'

sqr_brackets = '[', ']'

comparison_check = '<', '>', '!', '='

characters = {
    '^': operator.pow,
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '%': operator.mod,
    '+': operator.add,
    '-': operator.sub
}

all_functions = dict([(attr, getattr(math, attr)) for attr in dir(math) if callable(getattr(math, attr))])

all_functions['abs'] = abs

all_functions['round'] = round

constants = {
    'e': math.e,
    'pi': math.pi,
    'tau': math.tau,
    'inf': math.inf,
    'nan': math.nan
}

comparison = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt
}
