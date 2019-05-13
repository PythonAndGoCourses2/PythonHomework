"""Module to calculate result"""
from . import tokens
from . import exeptions


def calc(expr):
    """Calculate postfix string on stack"""
    stack = []
    for token in expr:
        if token in tokens.OPERATORS:
            try:
                op2, op1 = stack.pop(), stack.pop()
            except IndexError:
                raise exeptions.InvalidStringError()
            stack.append(tokens.OPERATORS[token].function(op1, op2))
        elif token in tokens.FUNCTIONS:
            if token in ('pow', 'log'):
                stack_copy = stack[:]
                try:
                    op2, op1 = stack_copy.pop(), stack_copy.pop()
                    stack_copy.append(tokens.FUNCTIONS[token](op1, op2))
                    stack = stack_copy[:]
                except IndexError:
                    operator = stack.pop()
                    stack.append(tokens.FUNCTIONS[token](operator))
            else:
                operator = stack.pop()
                stack.append(tokens.FUNCTIONS[token](operator))
        else:
            stack.append(float(token))
    if not len(stack) == 1:
        raise exeptions.InvalidStringError()
    return stack.pop()
