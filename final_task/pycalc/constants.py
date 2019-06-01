import math
import operator


CONSTANTS = {'pi': math.pi, 'tau': math.tau, 'e': math.e, 'inf': math.inf, 'nan': math.nan}

RIGHT_ASSOCIATIVITY_OPERATORS = {'^': 4, 'neg': 5, 'pos': 5}

LEFT_ASSOCIATIVITY_OPERATORS = {'<': 0, '<=': 0, '==': 0, '!=': 0, '>=': 0, '>': 0, '+': 2, '-': 2, '*': 3, '/': 3,
                                '//': 3, '%': 3}

PRIORITY = {**RIGHT_ASSOCIATIVITY_OPERATORS, ** LEFT_ASSOCIATIVITY_OPERATORS}


OPERATORS = {'<': operator.lt, '<=': operator.le, '==': operator.eq, '!=': operator.ne, '>=': operator.ge,
             '>': operator.gt, '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv,
             '//': operator.floordiv, '%': operator.mod, '^': operator.pow, 'neg': operator.neg,
             'pos': operator.pos}

FUNCTIONS = dict([(attr, getattr(math, attr)) for attr in dir(math) if callable(getattr(math, attr))])
FUNCTIONS['abs'] = abs
FUNCTIONS['round'] = round
