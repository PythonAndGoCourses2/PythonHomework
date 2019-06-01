from . import constants


def get_result(polish_notation):
    stack = []
    arg1 = ''
    for token in polish_notation:
        if token == 'neg' or token == 'pos':
            x = stack.pop()
            stack.append(constants.OPERATORS[token](x))
        elif token in constants.OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(constants.OPERATORS[token](x, y))
        elif token in constants.FUNCTIONS:
            if arg1:
                stack.append(constants.FUNCTIONS[token](arg1, stack.pop()))
            else:
                stack.append(constants.FUNCTIONS[token](stack.pop()))
        elif token == '[' or token == ']':
            continue
        elif token == ',':
            arg1 = stack.pop()
        else:
            stack.append(token)
    return stack[0]
