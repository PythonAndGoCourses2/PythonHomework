import sys
from Tokens import CONSTANTS, FUNCTIONS, func_delimiter, openBracket, closeBracket, OPERATORS

def get_postfix(input_string):
    output_string = []
    stack = [0]
    for index, token in enumerate(input_string):
        if is_number(token):
            output_string.append(token)
            continue
        if token in CONSTANTS:
            output_string.append(CONSTANTS[token])
            continue
        if token in FUNCTIONS:
            stack.append(token)
            continue
        if token == func_delimiter:
            while not stack[-1] == openBracket:
                output_string += stack.pop()
                if not stack:
                    print('ERROR: miss delimiter or open bracket')
                    sys.exit(1)
            continue
        if token in OPERATORS:
            if token == '-' or token == '+':
                if (not is_number(input_string[index - 1])) or not index:
                    output_string += '0'
            while (stack[-1] in OPERATORS) and (OPERATORS[token].priority <= OPERATORS[stack[-1]].priority):
                output_string += stack.pop()
            else:
                stack.append(token)
            continue
        if token == openBracket:
            stack.append(token)
            continue
        if token == closeBracket:
            while not stack[-1] == openBracket:
                output_string += stack.pop()
                if not stack:
                    print('ERROR: miss bracket')
                    sys.exit(1)
            stack.pop()
            if stack[-1] in FUNCTIONS:
                output_string += [stack.pop()]
            continue
        print(f'ERROR: no such function or operator: \'{token}\'')
        sys.exit(1)
    while stack[-1]:
        if stack[-1] == openBracket:
            print('ERROR: expected close bracket')
            sys.exit(1)
        if stack[-1] in OPERATORS:
            output_string += stack.pop()
    return output_string


def is_number(s):
    return s.isdigit()