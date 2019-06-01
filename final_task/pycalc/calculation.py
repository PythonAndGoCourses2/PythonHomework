from . import constants


def get_result(polish_notation_expression):
    stack = []
    arg1 = ''  # For functions with two arguments
    for item in polish_notation_expression:
        if item == 'neg' or item == 'pos':
            x = stack.pop()
            stack.append(constants.OPERATORS[item](x))
        elif item in constants.OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(constants.OPERATORS[item](x, y))
        elif item in constants.CONSTANTS:
            stack.append(constants.CONSTANTS[item])
        elif item in constants.FUNCTIONS:
            if arg1:
                stack.append(constants.FUNCTIONS[item](arg1, stack.pop()))
                arg1 = ''
            else:
                stack.append(constants.FUNCTIONS[item](stack.pop()))
        elif item == '[' or item == ']':
            continue
        elif item == ',':
            try:
                if arg1 != '':
                    raise Exception
                else:
                    arg1 = stack.pop()
            except Exception:
                print('ERROR: Something went wrong')
                break
        else:
            stack.append(item)
    try:
        if len(stack) > 1:
            raise Exception
        else:
            return stack[0]
    except Exception:
        print('ERROR: Something went wrong')
