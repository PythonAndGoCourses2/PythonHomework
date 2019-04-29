import math
import parser
import operator

OPERATORS = {'+': (1, operator.add),
             '-': (1, operator.sub),
             '*': (2, operator.mul),
             '/': (2, operator.truediv),
             '//': (2, operator.floordiv),
             '%': (2, operator.mod),
             '^': (3, operator.pow)}
math_const = {'e': math.e,
              'pi': math.pi}
math_function = dict([(attr, getattr(math, attr)) for attr in dir(math) if getattr(math, attr)])  # Need to redo


def parse(expression):
    number, func, op = '', '', ''
    for symbol in expression:

        if symbol.isalpha():
            func += symbol
        elif func in math_const:
            yield math_const[func]
            func = ''
        elif func in math_function:

            yield math_function[func]()

        if symbol.isdigit() or symbol == '.':
            number += symbol
        elif number:
            yield float(number)
            number = ''
        if symbol in OPERATORS:
            op += symbol
        elif op:
            yield op
            op = ''
        if symbol in "()":
            yield symbol
    if number:
        yield float(number)
    elif func and func in math_const:
        yield math_const[func]


def infix_to_postfix(parsed_formula):
    """This function translate infix form into postfix form"""
    stack = []
    for token in parsed_formula:
        if token in OPERATORS:
            while stack and stack[-1] != '(' and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                yield stack.pop()
            stack.append(token)
        elif token == ')':
            while stack:
                x = stack.pop()
                if x == '(':
                    break
                yield x
        elif token == "(":
            stack.append(token)
        else:
            yield token
    while stack:
        yield stack.pop()


def calc(polish):
    stack = []
    for token in polish:
        if token in OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(OPERATORS[token][1](x, y))
        else:
            stack.append(token)
    return stack[0]


def calculating(expression):
    return calc(infix_to_postfix(parse(expression)))


# print(calculating(parser.create_parser().EXPRESSION))
print(calculating("2+e"))
