from . import constants


def get_token(input_string):
    """Separation of tokens from the input string"""
    separated_input_string = ['']
    try:
        if input_string.count('(') != input_string.count(')'):
            raise Exception
        else:
            for char in input_string:
                if char.isdigit() and separated_input_string[-1].isdigit():
                    separated_input_string[-1] = separated_input_string[-1] + char
                elif char.isdigit() and '.' in separated_input_string[-1]:
                    separated_input_string[-1] = separated_input_string[-1] + char
                elif char.isdigit() and separated_input_string[-1].isalpha():
                    separated_input_string[-1] = separated_input_string[-1] + char
                elif char.isdigit() and separated_input_string[-1].isalnum():
                    separated_input_string[-1] = separated_input_string[-1] + char
                elif char == '.' and separated_input_string[-1].isdigit():
                    separated_input_string[-1] = separated_input_string[-1] + char
                elif char.isalpha() and separated_input_string[-1].isalnum():
                    separated_input_string[-1] = separated_input_string[-1] + char
                elif char in '+-/*%^=<>!':
                    if separated_input_string[-1] == '/':
                        separated_input_string[-1] = separated_input_string[-1] + char
                    elif separated_input_string[-1] in '<>!=':
                        separated_input_string[-1] = separated_input_string[-1] + char
                    else:
                        separated_input_string.append(char)
                else:
                    separated_input_string.append(char)
        if '' in separated_input_string:
            separated_input_string = separated_input_string[1:]
    except Exception:
        print('ERROR: Something went wrong')
    return separated_input_string


def separate_function(separated_input_string):
    """Selecting function arguments from a set of tokens"""
    processed_separated_input_string = ['']
    bracket_stack = []  # To define a closing bracket or end of function
    for item in separated_input_string:
        if item == '(':
            if processed_separated_input_string[-1].isalnum():  # Selection start of function
                processed_separated_input_string.append('[')
                bracket_stack.append('[')
            else:
                processed_separated_input_string.append(item)
                bracket_stack.append(item)
        elif item == ')':
            if bracket_stack.pop() == '[':  # Define a closing bracket or end of function
                processed_separated_input_string.append(']')
            else:
                processed_separated_input_string.append(item)
        else:
            processed_separated_input_string.append(item)
    return processed_separated_input_string[1:]


def create_infix_expression(processed_separated_input_string):
    """Adding unary operations and converting strings to numbers"""
    infix_expression = ['']
    for item in processed_separated_input_string:
        if item in constants.CONSTANTS:
            infix_expression.append(item)
        elif item == '-' and (infix_expression[-1] == '' or infix_expression[-1] in constants.OPERATORS or
                              infix_expression[-1] == '(' or infix_expression[-1] == '['):
            infix_expression.append('neg')
        elif item == '+' and (infix_expression[-1] == '' or infix_expression[-1] in constants.OPERATORS or
                              infix_expression[-1] == '(' or infix_expression[-1] == '['):
            infix_expression.append('pos')
        elif item.isdigit():
            infix_expression.append(float(item))
        elif item.isalnum() or item in '()[],':
            infix_expression.append(item)
        elif item.startswith('.'):
            infix_expression.append(float('0' + item))
        elif item in constants.OPERATORS:
            infix_expression.append(item)
        elif item == ' ':
            continue
        else:
            infix_expression.append(float(item))
    return infix_expression[1:]


def parse_input_string(input_string):
    """Issuing tokens"""
    infix_notation_expression = create_infix_expression(separate_function(get_token(input_string)))
    return infix_notation_expression
