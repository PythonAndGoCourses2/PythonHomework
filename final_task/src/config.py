STANDART_FUNCTIONS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "+": lambda a, b: a+b,
    "-": lambda a, b: a-b,
    "*": lambda a, b: a*b,
    "/": lambda a, b: a/b,
    "%": lambda a, b: a % b,
    "//": lambda a, b: a//b,
    "-unary": lambda a: -a,
    "+unary": lambda a: +a,
    "^": lambda a, b: a**b,
}
PRIORITIES = {
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

REGEX_SPEC_SYMBOLS = ["*", "+", "^"]
