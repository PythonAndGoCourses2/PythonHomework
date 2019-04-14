import math


def log(a):
    return math.log(a)


def exp(a):
    return math.exp(a)



functions = {
    "+": lambda a, b: a+b,
    "-": lambda a, b: a-b,
    "*": lambda a, b: a*b,
    "^": lambda a, b: a**b,
    "/": lambda a, b: a/b,
    "//": lambda a, b: a//b,
    "unary-": lambda a: -a,
    "unary+": lambda a: +a,
    "log": log,
    "exp": exp,
    "pi": math.pi,
    "abs": abs
}
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