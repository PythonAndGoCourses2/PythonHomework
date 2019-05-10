import sys
from . import Tokens as t


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
        if token in t.CONSTANTS:
            output_string.append(t.CONSTANTS[token])
            continue
        if token in t.FUNCTIONS:
            stack.append(token)
            continue
        if token == t.func_delimiter:
            while not stack[-1] == t.openBracket:
                output_string += [stack.pop()]
                if not stack:
                    print('ERROR: miss delimiter or open bracket')
                    sys.exit(1)
            continue
        if token in t.OPERATORS:
            if token == '-' or token == '+':
                if ((not is_number(input_string[index - 1])) or not index) and (
                        input_string[index - 1] != t.closeBracket):
                    if not input_string[index - 1] in t.CONSTANTS:
                        output_string += '0'
            while stack[-1] in t.OPERATORS and \
                    ((token in t.left_associativity and t.OPERATORS[token].priority <= t.OPERATORS[
                        stack[-1]].priority) or
                     (token in t.right_associativity and t.OPERATORS[token].priority < t.OPERATORS[
                         stack[-1]].priority)):
                output_string += [stack.pop()]
            else:
                stack.append(token)
            continue
        if token == t.openBracket:
            stack.append(token)
            continue
        if token == t.closeBracket:
            while not stack[-1] == t.openBracket:
                output_string += [stack.pop()]
                if not stack:
                    print('ERROR: miss bracket')
                    sys.exit(1)
            stack.pop()
            if stack[-1] in t.FUNCTIONS:
                output_string += [stack.pop()]
            continue
        print(f'ERROR: no such function or operator: \'{token}\'')
        sys.exit(1)
    while stack[-1]:
        if stack[-1] == t.openBracket:
            print('ERROR: expected close bracket')
            sys.exit(1)
        if stack[-1] in t.OPERATORS:
            output_string += [stack.pop()]
    return output_string


def is_number(s):
    if '.' in s:
        return True
    return s.isdigit()