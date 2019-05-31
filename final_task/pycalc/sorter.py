from . import constants


def create_polish_notation(parsed_formula):
    stack_operation = []
    stack_function = []
    polish_notation = []
    operation_counter = 0  # counting operations before a mathematical function
    keeper_operation_counter = [0]

    while parsed_formula:
        token = parsed_formula[0]
        parsed_formula = parsed_formula[1:]
        if token in constants.OPERATORS:
            while stack_operation and stack_operation[-1] != '(' and \
                    ((token in constants.LEFT_ASSOCIATIVITY_OPERATORS and constants.PRIORITY[token] <=
                        constants.PRIORITY[stack_operation[-1]]) or
                        (token in constants.RIGHT_ASSOCIATIVITY_OPERATORS and constants.PRIORITY[token] <
                            constants.PRIORITY[stack_operation[-1]])) and not stack_function:
                polish_notation.append(stack_operation.pop())
                operation_counter -= 1
            stack_operation.append(token)
            operation_counter += 1
        elif token == ')':
            while stack_operation:
                x = stack_operation.pop()
                if x == '(':
                    break
                polish_notation.append(x)
        elif token == '(':
            stack_operation.append(token)
        elif token in constants.FUNCTIONS:
            stack_function.append(token)
            keeper_operation_counter.append(operation_counter)
            print(keeper_operation_counter)
        elif token == '[':
            continue
        elif token == ']':
            print(operation_counter)
            print(stack_operation)
            for i in range(keeper_operation_counter[-1]-keeper_operation_counter[-2]):
                polish_notation.append(stack_operation.pop())
                operation_counter -= 1
            polish_notation.append(stack_function.pop())
        else:
            polish_notation.append(token)
    while stack_operation:
        polish_notation.append(stack_operation.pop())

    return polish_notation
