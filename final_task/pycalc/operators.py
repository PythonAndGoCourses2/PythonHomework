def degree(a, b):
    return float(a)**float(b)


def multiply(a, b):
    return a * b


def remainder(a, b):
    return a % b


def division(a, b):
    return a / b


def noremainer(a, b):
    return a // b


operators = {
    "^": degree,
    "*": multiply,
    "/": division,
    "%": remainder,
    "&": noremainer,
}
