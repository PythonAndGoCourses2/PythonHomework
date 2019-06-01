from . import constants


def create_polish_notation(infix_notation_expression):
    """Creating expression in polish notation"""
    stack_operation = []
    stack_function = []
    polish_notation_expression = []

    for token in infix_notation_expression:
        if token in constants.OPERATORS:
            while stack_operation and stack_operation[-1] != '(' and stack_operation[-1] != '[' and \
                    ((token in constants.LEFT_ASSOCIATIVITY_OPERATORS and constants.PRIORITY[token] <=
                        constants.PRIORITY[stack_operation[-1]]) or
                        (token in constants.RIGHT_ASSOCIATIVITY_OPERATORS and constants.PRIORITY[token] <
                            constants.PRIORITY[stack_operation[-1]])):
                polish_notation_expression.append(stack_operation.pop())
            stack_operation.append(token)
        elif token == ')':
            while stack_operation:
                x = stack_operation.pop()
                if x == '(':
                    break
                polish_notation_expression.append(x)
        elif token == ',':
            while stack_operation[-1] != '[':
                polish_notation_expression.append(stack_operation.pop())
            polish_notation_expression.append(token)
        elif token == '(':
            stack_operation.append(token)
        elif token in constants.CONSTANTS:
            polish_notation_expression.append(token)
        elif token in constants.FUNCTIONS:
            stack_function.append(token)
        elif token == '[':
            polish_notation_expression.append(token)
            stack_operation.append(token)
        elif token == ']':
            while stack_operation[-1] != '[':
                polish_notation_expression.append(stack_operation.pop())
            stack_operation.pop()
            polish_notation_expression.append(token)
            polish_notation_expression.append(stack_function.pop())
        else:
            polish_notation_expression.append(token)
    while stack_operation:
        polish_notation_expression.append(stack_operation.pop())
    return polish_notation_expression
