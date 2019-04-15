import math


def log(a):
    return math.log(a)


def exp(a):
    return math.exp(a)


functions = {attr: getattr(math, attr) for attr in dir(math) if callable(
    getattr(math, attr)) or type(getattr(math, attr)) == float}
priorities = {
    "==": 0,
    "!=": 0,
    ">": 1,
    ">=": 1,
    "<": 1,
    "<=": 1,
    "+": 2,
    "-": 2,
    "*": 3,
    "/": 3,
    "//": 3,
    "%": 3,
    "unary-": 4,
    "unary+": 4,
    "^": 5
}

regexSpecialSymbols = ["*", "+", "^"]
