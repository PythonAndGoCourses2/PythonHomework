from . import constants
import sys

def get_token(input_expression):
    """Getting a tokens from input string"""
    try:
        if input_expression.count('(') != input_expression.count(')'):
            raise Exception
        else:
            raw_tokens = ['']
            for char in input_expression:
                if char.isdigit() and raw_tokens[-1].isdigit():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char == '.' and raw_tokens[-1].isdigit():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char.isdigit() and '.' in raw_tokens[-1]:
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char.isalpha() and raw_tokens[-1].isalnum():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char.isdigit() and raw_tokens[-1].isalpha():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char.isdigit() and raw_tokens[-1].isalnum():
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char == '/' and raw_tokens[-1] == '/':
                    raw_tokens[-1] = raw_tokens[-1] + char
                elif char == '=' and raw_tokens[-1] in '<>!=':
                    raw_tokens[-1] = raw_tokens[-1] + char
                else:
                    raw_tokens.append(char)
    except:
        print('ERROR: Something went wrong')
    return raw_tokens[1:]


def separate_function(raw_tokens):
    """Selecting function arguments"""
    tokens = ['']
    stack = []  # To define a closing bracket or end of function
    while raw_tokens:
        token = raw_tokens[0]
        raw_tokens = raw_tokens[1:]
        if token == '(':
            if tokens[-1].isalnum():  # Selection start of function
                tokens.append('[')
                stack.append('[')
            else:
                tokens.append(token)
                stack.append(token)
        elif token == ')':
            x = stack.pop()
            if x == '[':  # Define a closing bracket or end of function
                tokens.append(']')
            else:
                tokens.append(token)
        else:
            tokens.append(token)
    return tokens[1:]


def create_infix(tokens):
    """Adding unary operations, constants and converting strings to numbers"""
    infix = ['']
    while tokens:
        token = tokens[0]
        tokens = tokens[1:]
        if token in constants.CONSTANTS:
            infix.append(constants.CONSTANTS[token])
        elif token == '-' and (infix[-1] == '' or infix[-1] in constants.OPERATORS):
            infix.append('neg')
        elif token == '+' and (infix[-1] == '' or infix[-1] in constants.OPERATORS):
            infix.append('pos')
        elif token.isnumeric():
            infix.append(float(token))
        else:
            infix.append(token)
    return infix[1:]


def parse_input_expression(input_string):
    """Issuing tokens"""
    return create_infix(separate_function(get_token(input_string)))
