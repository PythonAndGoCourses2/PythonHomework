from . import constants


def create_polish_notation(parsed_formula):
    stack_operation = []
    stack_function = []
    raw_polish_notation = []

    while parsed_formula:
        token = parsed_formula[0]
        parsed_formula = parsed_formula[1:]
        if token in constants.OPERATORS:
            while stack_operation and stack_operation[-1] != '(' and stack_operation[-1] != '[' and \
                    ((token in constants.LEFT_ASSOCIATIVITY_OPERATORS and constants.PRIORITY[token] <=
                        constants.PRIORITY[stack_operation[-1]]) or
                        (token in constants.RIGHT_ASSOCIATIVITY_OPERATORS and constants.PRIORITY[token] <
                            constants.PRIORITY[stack_operation[-1]])) and not stack_function:
                raw_polish_notation.append(stack_operation.pop())
            stack_operation.append(token)

        elif token == ')':
            while stack_operation:
                x = stack_operation.pop()
                if x == '(':
                    break
                raw_polish_notation.append(x)
        elif token == ',':
            while stack_operation[-1] != '[':
                raw_polish_notation.append(stack_operation.pop())
            raw_polish_notation.append(token)

        elif token == '(':
            stack_operation.append(token)
        elif token in constants.FUNCTIONS:
            stack_function.append(token)
        elif token == '[':
            raw_polish_notation.append(token)
            stack_operation.append(token)
        elif token == ']':
            while stack_operation[-1] != '[':
                raw_polish_notation.append(stack_operation.pop())
            stack_operation.pop()
            raw_polish_notation.append(token)
            raw_polish_notation.append(stack_function.pop())
        else:
            raw_polish_notation.append(token)
    while stack_operation:
        raw_polish_notation.append(stack_operation.pop())

    return raw_polish_notation
