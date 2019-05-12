from . import tokens
from . import exeptions


def calc(expr):
    stack = []
    for token in expr:
        if token in tokens.OPERATORS:
            op2, op1 = stack.pop(), stack.pop()
            stack.append(tokens.OPERATORS[token].function(op1, op2))
        elif token in tokens.FUNCTIONS:
            if token == 'pow' or token == 'log':
                stack_copy = stack[:]
                try:
                    op2, op1 = stack_copy.pop(), stack_copy.pop()
                    stack_copy.append(tokens.FUNCTIONS[token](op1, op2))
                    stack = stack_copy[:]
                except Exception:
                    op = stack.pop()
                    stack.append(tokens.FUNCTIONS[token](op))
            else:
                op = stack.pop()
                stack.append(tokens.FUNCTIONS[token](op))
        else:
            stack.append(float(token))
    if not len(stack) == 1:
        raise exeptions.InvalidStringError()
    return stack.pop()
