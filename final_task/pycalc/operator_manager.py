import math
import operator


def create_func_dict():
    func_dict = {
                'abs': {'operator': abs, 'priority': 0},
                'round': {'operator': round, 'priority': 0}
                }
    for k, v in math.__dict__.items():
        if k.startswith('_'):
            continue
        func_dict[k] = {'operator': v, 'priority': 0}
    return func_dict


function_dict = create_func_dict()

operator_dict = {
    '+': {'operator': operator.add, 'priority': 4},
    '-': {'operator': operator.sub, 'priority': 4},
    '/': {'operator': operator.truediv, 'priority': 3},
    '*': {'operator': operator.mul, 'priority': 3},
    '%': {'operator': operator.mod, 'priority': 3},
    '//': {'operator': operator.floordiv, 'priority': 3},
    '^': {'operator': operator.pow, 'priority': 1},
    '**': {'operator': operator.pow, 'priority': 1},
    '==': {'operator': operator.eq, 'priority': 5},
    '!=': {'operator': operator.ne, 'priority': 5},
    '>': {'operator': operator.gt, 'priority': 5},
    '<': {'operator': operator.lt, 'priority': 5},
    '>=': {'operator': operator.ge, 'priority': 5},
    '<=': {'operator': operator.le, 'priority': 5},
}

unary_dict = {
    '-': {'operator': operator.sub, 'priority': 2}
}
