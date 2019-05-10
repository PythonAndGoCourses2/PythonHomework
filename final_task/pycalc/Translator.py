import sys
from . import Tokens


# from Tokens import CONSTANTS, FUNCTIONS, func_delimiter, openBracket, closeBracket, OPERATORS

def get_postfix(input_string):
    output_string = []
    stack = [0]
    for index, token in enumerate(input_string):
        if '.' in token:
            output_string.append(float(token))
            continue
        if is_number(token):
            output_string.append(token)
            continue
        if token in Tokens.CONSTANTS:
            output_string.append(Tokens.CONSTANTS[token])
            continue
        if token in Tokens.FUNCTIONS:
            stack.append(token)
            continue
        if token == Tokens.func_delimiter:
            while not stack[-1] == Tokens.openBracket:
                output_string += stack.pop()
                if not stack:
                    print('ERROR: miss delimiter or open bracket')
                    sys.exit(1)
            continue
        if token in Tokens.OPERATORS:
            if token == '-' or token == '+':
                if (not is_number(input_string[index - 1])) or not index:
                    if not input_string[index - 1] in Tokens.CONSTANTS:
                        output_string += '0'
            while (stack[-1] in Tokens.OPERATORS) and (
                    Tokens.OPERATORS[token].priority <= Tokens.OPERATORS[stack[-1]].priority):
                output_string += stack.pop()
            else:
                stack.append(token)
            continue
        if token == Tokens.openBracket:
            stack.append(token)
            continue
        if token == Tokens.closeBracket:
            while not stack[-1] == Tokens.openBracket:
                output_string += stack.pop()
                if not stack:
                    print('ERROR: miss bracket')
                    sys.exit(1)
            stack.pop()
            if stack[-1] in Tokens.FUNCTIONS:
                output_string += [stack.pop()]
            continue
        print(f'ERROR: no such function or operator: \'{token}\'')
        sys.exit(1)
    while stack[-1]:
        if stack[-1] == Tokens.openBracket:
            print('ERROR: expected close bracket')
            sys.exit(1)
        if stack[-1] in Tokens.OPERATORS:
            output_string += stack.pop()
    return output_string


def is_number(s):
    return s.isdigit()