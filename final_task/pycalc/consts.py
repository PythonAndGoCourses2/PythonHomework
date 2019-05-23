import operator
import math

signs = ['+', '-', '*', '/', '^', '%', '>', '<', '=', '//', '!']

logical_signs = {
    '>': operator.gt,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne,
    "<=": operator.le,
    "<": operator.le
}


operators_type1 = {
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '%': operator.mod
}

operators_main = {
    '+': operator.add,
    '-': operator.sub
}

math_consts = {
    "pi": math.pi,
    "e": math.e

}
