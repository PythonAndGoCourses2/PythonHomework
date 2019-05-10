from . import Tokens


def calc(expr):
    stack = [0]
    for token in expr:
        if token in Tokens.OPERATORS:
            op2, op1 = stack.pop(), stack.pop()
            stack.append(Tokens.OPERATORS[token].function(op1, op2))
        elif token in Tokens.FUNCTIONS:
            if token == 'pow' or token == 'log':
                op2, op1 = stack.pop(), stack.pop()
                try:
                    stack.append(Tokens.FUNCTIONS[token](op1, op2))
                except ValueError:
                    stack.append(op1)
                    stack.append(Tokens.FUNCTIONS[token](op2))
            else:
                op = stack.pop()
                stack.append(Tokens.FUNCTIONS[token](op))
        else:
            stack.append(float(token))
    return stack.pop()
