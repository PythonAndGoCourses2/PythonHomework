from . import constants


def create_polish_notation(infix_notation_expression):
    """Creating expression in polish notation"""
    stack_operation = []
    stack_function = []
    polish_notation_expression = []

    for item in infix_notation_expression:
        if item in constants.OPERATORS:
            while stack_operation and stack_operation[-1] != '(' and stack_operation[-1] != '[' and \
                    ((item in constants.LEFT_ASSOCIATIVITY_OPERATORS and constants.PRIORITY[item] <=
                      constants.PRIORITY[stack_operation[-1]]) or
                        (item in constants.RIGHT_ASSOCIATIVITY_OPERATORS and constants.PRIORITY[item] <
                         constants.PRIORITY[stack_operation[-1]])):
                polish_notation_expression.append(stack_operation.pop())
            stack_operation.append(item)
        elif item == ')':
            while stack_operation:
                x = stack_operation.pop()
                if x == '(':
                    break
                polish_notation_expression.append(x)
        elif item == ',':
            while stack_operation[-1] != '[':
                polish_notation_expression.append(stack_operation.pop())
            polish_notation_expression.append(item)
        elif item == '(':
            stack_operation.append(item)
        elif item in constants.CONSTANTS:
            polish_notation_expression.append(item)
        elif item in constants.FUNCTIONS:
            stack_function.append(item)
        elif item == '[':
            polish_notation_expression.append(item)
            stack_operation.append(item)
        elif item == ']':
            while stack_operation[-1] != '[':
                polish_notation_expression.append(stack_operation.pop())
            stack_operation.pop()
            polish_notation_expression.append(item)
            polish_notation_expression.append(stack_function.pop())
        else:
            polish_notation_expression.append(item)
    while stack_operation:
        polish_notation_expression.append(stack_operation.pop())
    return polish_notation_expression
