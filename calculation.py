import constants


def calc(polish):
    stack = []
    for token in polish:
        if token == 'neg' or token == 'pos':
            x = stack.pop()
            stack.append(constants.OPERATORS[token](x))
        elif token in constants.OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(constants.OPERATORS[token](x, y))
        elif token in constants.FUNCTIONS:
            x = stack.pop()
            stack.append(constants.FUNCTIONS[token](x))
        else:
            stack.append(token)
    return stack[0]