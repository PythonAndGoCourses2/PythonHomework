import math
from collections import namedtuple

"""
Definitions for all type of input
"""
Operator = namedtuple("Operator", ["LAssos", "priority", "func"])
Constant = namedtuple("Constant", ["value"])
_functions = {
    attr: getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))
}

_functions["abs"] = abs
_functions["round"] = round
_number = r"\d*[\.]?\d+"
_operators = {
    "^": Operator(LAssos=False, priority=4, func=lambda x, y: x ** y),
    "*": Operator(LAssos=True, priority=3, func=lambda x, y: x * y),
    "/": Operator(LAssos=True, priority=3, func=lambda x, y: x / y),
    "//": Operator(LAssos=True, priority=3, func=lambda x, y: x // y),
    "%": Operator(LAssos=True, priority=3, func=lambda x, y: x % y),
    "+": Operator(LAssos=True, priority=2, func=lambda x, y: x + y),
    "-": Operator(LAssos=True, priority=2, func=lambda x, y: x - y),
    "==": Operator(LAssos=True, priority=1, func=lambda x, y: x == y),
    "<=": Operator(LAssos=True, priority=1, func=lambda x, y: x <= y),
    ">=": Operator(LAssos=True, priority=1, func=lambda x, y: x >= y),
    "<": Operator(LAssos=True, priority=1, func=lambda x, y: x < y),
    ">": Operator(LAssos=True, priority=1, func=lambda x, y: x > y),
    "!=": Operator(LAssos=True, priority=1, func=lambda x, y: x != y),
}

_constants = {
    "e": Constant(value=math.e),
    "pi": Constant(value=math.pi),
    "tau": Constant(value=math.tau),
}
