from . import constants


def get_token(input_string):
    """Separation of tokens from the input string"""
    raw_tokens = ['']
    try:
        if input_string.count('(') != input_string.count(')'):
            raise Exception
        else:
            for char in input_string:
                if char.isdigit() and raw_tokens[-1].isdigit():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char.isdigit() and '.' in raw_tokens[-1]:
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char.isdigit() and raw_tokens[-1].isalpha():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char.isdigit() and raw_tokens[-1].isalnum():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char == '.' and raw_tokens[-1].isdigit():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char.isalpha() and raw_tokens[-1].isalnum():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char in '+-/*%^=<>!':
                    if raw_tokens[-1] == '/':
                        raw_tokens[-1] = raw_tokens[-1] + char
                    elif raw_tokens[-1] in '<>!=':
                        raw_tokens[-1] = raw_tokens[-1] + char
                    else:
                        raw_tokens.append(char)
                else:
                    raw_tokens.append(char)
        if '' in raw_tokens:
            raw_tokens = raw_tokens[1:]
    except Exception:
        print('ERROR: Something went wrong')
    return raw_tokens


def separate_function(raw_tokens):
    """Selecting function arguments from a set of tokens"""
    tokens = ['']
    bracket_stack = []  # To define a closing bracket or end of function
    for token in raw_tokens:
        if token == '(':
            if tokens[-1].isalnum():  # Selection start of function
                tokens.append('[')
                bracket_stack.append('[')
            else:
                tokens.append(token)
                bracket_stack.append(token)
        elif token == ')':
            if bracket_stack.pop() == '[':  # Define a closing bracket or end of function
                tokens.append(']')
            else:
                tokens.append(token)
        else:
            tokens.append(token)
    return tokens[1:]


def create_infix_expression(tokens):
    """Adding unary operations and converting strings to numbers"""
    infix_expression = ['']
    for token in tokens:
        if token in constants.CONSTANTS:
            infix_expression.append(token)
        elif token == '-' and (infix_expression[-1] == '' or infix_expression[-1] in constants.OPERATORS or
                               infix_expression[-1] == '(' or infix_expression[-1] == '['):
            infix_expression.append('neg')
        elif token == '+' and (infix_expression[-1] == '' or infix_expression[-1] in constants.OPERATORS or
                               infix_expression[-1] == '(' or infix_expression[-1] == '['):
            infix_expression.append('pos')
        elif token.isdigit():
            infix_expression.append(float(token))
        elif token.isalnum() or token in '()[],':
            infix_expression.append(token)
        elif token.startswith('.'):
            infix_expression.append(float('0' + token))
        elif token in constants.OPERATORS:
            infix_expression.append(token)
        elif token == ' ':
            continue
        else:
            infix_expression.append(float(token))
    return infix_expression[1:]


def parse_input_string(input_string):
    """Issuing tokens"""
    infix_notation_expression = create_infix_expression(separate_function(get_token(input_string)))
    return infix_notation_expression
