from . import constants


def get_result(polish_notation):
    stack = []
    for token in polish_notation:
        if token == 'neg' or token == 'pos':
            x = stack.pop()
            stack.append(constants.OPERATORS[token](x))
            print(stack)
        elif token in constants.OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(constants.OPERATORS[token](x, y))
        elif token in constants.FUNCTIONS:
            x = stack.pop()
            stack.append(constants.FUNCTIONS[token](x))
        elif token == '[' or token == ']':
            continue
        else:
            stack.append(token)
    return stack[0]
