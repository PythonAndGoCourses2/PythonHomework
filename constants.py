import math
import operator


CONSTANTS = {'pi': math.pi, 'tau': math.tau, 'e': math.e, 'inf': math.inf, 'nan': math.nan}

OPERATION_PRIORITY = {'<': 1, '<=': 1, '==': 1, '!=': 1, '>=': 2, '>': 1,
                      '+': 2, '-': 2, '*': 3, '/': 3, '//': 3, '%': 3, '^': 4,
                      'neg': 5, 'pos': 5}

OPERATORS = {'<': operator.lt, '<=': operator.le, '==': operator.eq, '!=': operator.ne, '>=': operator.ge,
             '>': operator.gt, '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv,
             '//': operator.floordiv, '%': operator.mod, '^': operator.pow, 'neg': operator.neg,
             'pos': operator.pos}

FUNCTIONS = math.__dict__
FUNCTIONS['abs'] = abs
FUNCTIONS['round'] = round
