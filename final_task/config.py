import operator
import math

operands = {'^': operator.pow,
            '*': operator.mul,
            '/': operator.truediv,
            '//': operator.floordiv,
            '%': operator.mod,
            '+': operator.add,
            '-': operator.sub
            }

priorities = {'^': 3,
              '*': 2,
              '/': 2,
              '//': 2,
              '%': 2,
              '+': 1,
              '-': 1
              }


constants = {'pi': math.pi,
             'e': math.e,
             'tau': math.tau,
             'inf': math.inf,
             'nan': math.nan
             }

comparison = ['<', '>', '!', '=']

function = dict([(attr, getattr(math, attr)) for attr in dir(math) if callable(getattr(math, attr))])

function['abs'] = abs
function['round'] = round
