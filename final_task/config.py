import math
import operator


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
all_functions = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
    'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
    'asinh': math.asinh, 'acosh': math.acosh, 'atanh': math.atanh,
    'hypot': math.hypot, 'degrees': math.degrees, 'radians': math.radians,
    'ceil': math.ceil, 'copysign': math.copysign, 'fabs': math.fabs,
    'factorial': math.factorial, 'floor': math.floor, 'fmod': math.fmod,
    'frexp': math.frexp, 'ldexp': math.ldexp, 'fsum': math.fsum,
    'isfinite': math.isfinite, 'isinf': math.isinf, 'isnan': math.isnan,
    'modf': math.modf, 'trunc': math.trunc, 'exp': math.exp,
    'expm1': math.expm1, 'log': math.log, 'log1p': math.log1p,
    'log10': math.log10, 'log2': math.log2, 'pow': math.pow,
    'sqrt': math.sqrt, 'erf': math.erf, 'erfc': math.erfc,
    'gamma': math.gamma, 'lgamma': math.lgamma, 'abs': abs, 'round': round
}
constants = {
    'e': math.e,
    'pi': math.pi,
    'tau': math.tau
}
comparison = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt
}
