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
        elif token in constants.CONSTANTS:
            stack.append(constants.CONSTANTS[token])
        elif token in constants.FUNCTIONS:
            if arg1:
                stack.append(constants.FUNCTIONS[token](arg1, stack.pop()))
                arg1 = ''
            else:
                stack.append(constants.FUNCTIONS[token](stack.pop()))
        elif token == '[' or token == ']':
            continue
        elif token == ',':
            try:
                if arg1 != '':
                    raise Exception
                else:
                    arg1 = stack.pop()
            except Exception:
                print('ERROR: Something went wrong')
                break
        else:
            stack.append(token)
    try:
        if len(stack) > 1:
            raise Exception
        else:
            return stack[0]
    except Exception:
        print('ERROR: Something went wrong')
