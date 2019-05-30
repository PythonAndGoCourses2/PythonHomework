import sys
import math


CONSTANTS = ('pi', 'tau', 'e', 'inf', 'nan')
OPERATORS = ('+', '-', '*', '/', '//', '%', '^', '<', '<=', '==', '!=', '>=', '>', '(', 'neg', 'pos', '[')


def get_token(input_expression):
    """Getting a tokens from input string"""
    if input_expression.count('(') != input_expression.count(')'):
        print('ERROR: the number of opening and closing brackets must match')
        sys.exit(1)
    else:
        raw_tokens = ['']
        for i in input_expression:
            if i.isdigit() and raw_tokens[-1].isdigit():
                raw_tokens[-1] = raw_tokens[-1]+i
            elif i == '.' and raw_tokens[-1].isdigit():
                raw_tokens[-1] = raw_tokens[-1] + i
            elif i.isdigit() and '.' in raw_tokens[-1]:
                raw_tokens[-1] = raw_tokens[-1] + i
            elif i.isalpha() and raw_tokens[-1].isalnum():
                raw_tokens[-1] = raw_tokens[-1] + i
            elif i.isdigit() and raw_tokens[-1].isalpha():
                raw_tokens[-1] = raw_tokens[-1] + i
            elif i.isdigit() and raw_tokens[-1].isalnum():
                raw_tokens[-1] = raw_tokens[-1] + i
            elif i == '/' and raw_tokens[-1] == '/':
                raw_tokens[-1] = raw_tokens[-1] + i
            elif i == '=' and raw_tokens[-1] in '<>!=':
                raw_tokens[-1] = raw_tokens[-1] + i
            else:
                raw_tokens.append(i)
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
        if token in CONSTANTS:
            infix.append(math.__dict__[token])
        elif token == '-' and (infix[-1] == '' or infix[-1] in OPERATORS):
            infix.append('neg')
        elif token == '+' and (infix[-1] == '' or infix[-1] in OPERATORS):
            infix.append('pos')
        elif token.isnumeric():
            infix.append(float(token))
        else:
            infix.append(token)
    return infix[1:]


def parse_input_expression(input_string):
    """Issuing tokens"""
    return create_infix(separate_function(get_token(input_string)))
