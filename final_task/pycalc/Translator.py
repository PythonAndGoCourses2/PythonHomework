import sys
from . import Tokens as t


def get_postfix(input_string):
    input_string = check_unars(input_string)
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
            # if token == '-' or token == '+':
            #     if is_unar(input_string[index - 1], index):
            #         output_string += '0'
            # if ((not is_number(input_string[index - 1])) or not index) and (
            #         input_string[index - 1] != t.closeBracket):
            #     if not input_string[index - 1] in t.CONSTANTS:
            #         output_string += '0'
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


def check_unars(infix_string):
    output_string = list()
    prev_unar = False
    bracket_counter = 0
    for index, token in enumerate(infix_string):
        if token in t.OPERATORS:
            if token == '-' or token == '+':
                if is_unar(infix_string, index):
                    # if not infix_string[index +1] in t.FUNCTIONS:
                    #     output_string.append('(')
                    #     prev_unar = True
                    #     bracket_counter += 1
                    if infix_string[index - 1] in t.OPERATORS and \
                            t.OPERATORS[infix_string[index - 1]].priority > t.OPERATORS[token].priority:
                        output_string.append('(')
                        prev_unar = True
                        bracket_counter += 1
                    output_string.append('0')
                    output_string.append(token)
                    continue
        output_string.append(token)
        if prev_unar:
            for i in range(bracket_counter):
                output_string.append(')')
                bracket_counter -= 1
            prev_unar = False

    return output_string


def is_unar(s, index):
    s = s[index - 1]
    return (s in t.OPERATORS or
            s in t.FUNCTIONS or
            s == t.func_delimiter or
            not index or
            s == t.openBracket)
