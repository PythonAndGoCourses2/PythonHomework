"""Module to calculate result"""
from pycalc.library import Library as lib
from pycalc import exeptions


def calculate(expr):
    """Calculate postfix string on stack"""
    stack = []
    unary_operators = (lib.UNARY_PLUS, lib.UNARY_MINUS)
    for token in expr:
        try:
            if token == lib.FUNC_DELIMITER:
                stack.append(token)
            elif token == lib.FILLER:
                stack.append(token)
            elif token in lib.OPERATORS:
                if token in unary_operators:
                    operator = stack.pop()
                    stack.append(lib.OPERATORS[token].function(operator))
                    continue
                op2, op1 = stack.pop(), stack.pop()
                stack.append(lib.OPERATORS[token].function(op1, op2))
            elif token in lib.user_functions:
                calculate_function(lib.user_functions, token, stack)
            elif token in lib.FUNCTIONS:
                calculate_function(lib.FUNCTIONS, token, stack)
            else:
                stack.append(float(token))
        except IndexError:
            raise exeptions.InvalidStringError('not balanced operators and operands')
    if len(stack) != 1:
        raise exeptions.InvalidStringError('not balanced operators and operands')
    return stack.pop()


def calculate_function(functions, token, stack):
    """Calculate token as one of functions function"""
    operators = []
    if stack[-1] == lib.FILLER:
        stack.pop()
        stack.append(float(functions[token]()))
    else:
        while len(stack) >= 2 and stack[-2] == lib.FUNC_DELIMITER:
            operators.append(stack.pop())
            stack.pop()
        operators.append(stack.pop())
        operators.reverse()
        stack.append(float(functions[token](*operators)))
