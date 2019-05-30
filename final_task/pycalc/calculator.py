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
            elif token == library.FUNC_DELIMITER:
                stack.append(token)
            elif token in library.FUNCTIONS:
                operators = []
                while len(stack) >= 2 and stack[-2] == library.FUNC_DELIMITER:
                    operators.append(stack.pop())
                    stack.pop()
                operators.append(stack.pop())
                operators.reverse()
                stack.append(library.FUNCTIONS[token](*operators))
                # if count_args(token) == 2 and len(stack) >= 2:
                #     op2, op1 = stack.pop(), stack.pop()
                #     stack.append(library.FUNCTIONS[token](op1, op2))
                # elif count_args(token) == 1 or len(stack) >= 1:
                #     operator = stack.pop()
                #     stack.append(library.FUNCTIONS[token](operator))
                # else:
                #     stack.append(library.FUNCTIONS[token]())
            else:
                stack.append(float(token))
        except IndexError:
            raise exeptions.InvalidStringError('not balanced operators and operands')
    if len(stack) != 1:
        raise exeptions.InvalidStringError('not balanced operators and operands')
    return stack.pop()


def count_args(func):
    """Returns number of function arguments"""
    specification = library.FUNCTIONS[func].__doc__.split('\n')[0]
    arguments = specification[specification.find('(') + 1:specification.find(')')]
    return arguments.count(',') + 1 if arguments else 0
