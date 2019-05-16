"""Module to calculate result"""
from pycalc import library
from pycalc import exeptions


def calculate(expr):
    """Calculate postfix string on stack"""
    stack = []
    unary_operators = (library.UNARY_PLUS, library.UNARY_MINUS)
    for token in expr:
        try:
            if token in library.OPERATORS:
                if token in unary_operators:
                    operator = stack.pop()
                    stack.append(library.OPERATORS[token].function(operator))
                    continue
                op2, op1 = stack.pop(), stack.pop()
                stack.append(library.OPERATORS[token].function(op1, op2))
            elif token in library.FUNCTIONS:
                if count_args(token) == 2 and len(stack) >= 2:
                    op2, op1 = stack.pop(), stack.pop()
                    stack.append(library.FUNCTIONS[token](op1, op2))
                else:
                    operator = stack.pop()
                    stack.append(library.FUNCTIONS[token](operator))
            else:
                stack.append(float(token))
        except IndexError:
            raise exeptions.InvalidStringError('not balanced operators and operands')
    if not len(stack) == 1:
        raise exeptions.InvalidStringError('not balanced operators and operands')
    return stack.pop()


def count_args(func):
    """Returns number of function arguments"""
    spec = library.FUNCTIONS[func].__doc__.split('\n')[0]
    arg = spec[spec.find('(') + 1:spec.find(')')]
    return arg.count(',') + 1 if arg else 0
