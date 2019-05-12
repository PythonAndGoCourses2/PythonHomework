from . import Tokens
from . import Exeptions


def calc(expr):
    stack = []
    for token in expr:
        if token in Tokens.OPERATORS:
            op2, op1 = stack.pop(), stack.pop()
            stack.append(Tokens.OPERATORS[token].function(op1, op2))
        elif token in Tokens.FUNCTIONS:
            if token == 'pow' or token == 'log':
                stack_copy = stack[:]
                try:
                    op2, op1 = stack_copy.pop(), stack_copy.pop()
                    stack_copy.append(Tokens.FUNCTIONS[token](op1, op2))
                    stack = stack_copy[:]
                except Exception:
                    op = stack.pop()
                    stack.append(Tokens.FUNCTIONS[token](op))
            else:
                op = stack.pop()
                stack.append(Tokens.FUNCTIONS[token](op))
        else:
            stack.append(float(token))
    if not len(stack) == 1:
        raise Exeptions.InvalidStringError()
    return stack.pop()
    # try:
    #     stack = []
    #     for token in expr:
    #         if token in Tokens.OPERATORS:
    #             op2, op1 = stack.pop(), stack.pop()
    #             stack.append(Tokens.OPERATORS[token].function(op1, op2))
    #         elif token in Tokens.FUNCTIONS:
    #             if token == 'pow' or token == 'log':
    #                 stack_copy = stack[:]
    #                 try:
    #                     op2, op1 = stack_copy.pop(), stack_copy.pop()
    #                     stack_copy.append(Tokens.FUNCTIONS[token](op1, op2))
    #                     stack = stack_copy[:]
    #                 except Exception:
    #                     op = stack.pop()
    #                     stack.append(Tokens.FUNCTIONS[token](op))
    #             else:
    #                 op = stack.pop()
    #                 stack.append(Tokens.FUNCTIONS[token](op))
    #         else:
    #             stack.append(float(token))
    #     if not len(stack) == 1:
    #         raise Exeptions.InvalidStringError()
    #     return stack.pop()
    # except Exeptions.InvalidStringError:
    #     print('ERROR: invalid string input')
    #     exit(1)
    # except Exception:
    #     print('ERROR: something went wrong')
    #     exit(1)
