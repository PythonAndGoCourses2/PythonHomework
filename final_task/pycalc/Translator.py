import sys
from . import Tokens as t
from . import Exeptions


def get_postfix(input_string):
    """Translate infix notation into postfix

    Returns list of tokens"""
    input_string = make_valid(input_string)
    output_string = []
    stack = [0]
    try:
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
                        raise Exeptions.BracketsError()
                continue
            if token in t.OPERATORS:
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
                        raise Exeptions.BracketsError()
                stack.pop()
                if stack[-1] in t.FUNCTIONS:
                    output_string += [stack.pop()]
                continue
            raise Exeptions.UnknownFunctionError(token)
        while stack[-1]:
            if stack[-1] == t.openBracket:
                raise Exeptions.BracketsError()
            if stack[-1] in t.OPERATORS:
                output_string += [stack.pop()]
        return output_string
    except Exeptions.BracketsError:
        print('ERROR: brackets are not balanced')
        exit(1)
    except Exeptions.UnknownFunctionError as ex:
        print(f'ERROR: no such function or operator: \'{ex.token}\'')
        exit(1)
    except Exception:
        print('ERROR: something went wrong')
        exit(1)


def make_valid(expression):
    try:
        expression = dell_spaces(expression)
        expression = make_unarys(expression)
        chek_invalid_func(expression)
        return expression
    except Exeptions.InvalidStringError:
        print('ERROR: invalid string input')
        exit(1)
    except Exception:
        print('ERROR: something went wrong')
        exit(1)


def is_number(s):
    """Check if s is number"""
    if '.' in s:
        return True
    return s.isdigit()


def make_unarys(infix_string):
    """Translate unary operators in list

    into '0 operator operand'"""
    output_string = list()
    prev_unary = False
    bracket_counter = 0
    for index, token in enumerate(infix_string):
        if token in t.OPERATORS:
            if token == '-' or token == '+':
                if is_unary(infix_string, index):
                    if infix_string[index - 1] in t.OPERATORS and \
                            t.OPERATORS[infix_string[index - 1]].priority > t.OPERATORS[token].priority:
                        output_string.append('(')
                        prev_unary = True
                        bracket_counter += 1
                    output_string.append('0')
                    output_string.append(token)
                    continue
        output_string.append(token)
        if prev_unary:
            for i in range(bracket_counter):
                output_string.append(')')
                bracket_counter -= 1
            prev_unary = False
    return output_string


def is_unary(s, index):
    """Check if operator in s with index is unary"""
    token = s[index - 1]
    if token == ' ':
        token = s[index - 2]
    return (token in t.OPERATORS or
            token in t.FUNCTIONS or
            token == t.func_delimiter or
            not index or
            token == t.openBracket)


def chek_invalid_func(tokens):
    """Check for all func tokens valid"""
    for index, token in enumerate(tokens):
        if token in t.FUNCTIONS:
            if len(tokens) <= 1:
                raise Exeptions.InvalidStringError()
            elif is_number(tokens[index + 1]):
                raise Exeptions.InvalidStringError()


def dell_spaces(tokens):
    """Delete all space tokens"""
    no_spaces_tokens = []
    for index, token in enumerate(tokens):
        if token == ' ':
            if is_number(tokens[index - 1]) and is_number(tokens[index + 1]):
                raise Exeptions.InvalidStringError()
            else:
                continue
        else:
            no_spaces_tokens.append(token)
    return no_spaces_tokens
