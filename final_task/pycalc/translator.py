"""Module contains functions to translate infix notation into postfix"""
from pycalc import tokens as t
from pycalc import exeptions


def get_postfix(input_string):
    """Translate infix notation into postfix

    Returns list of tokens"""
    input_string = make_valid(input_string)
    output_string = []
    stack = [0]
    for token in input_string:
        if is_number(token):
            output_string.append(float(token))
            continue
        if token in t.CONSTANTS:
            output_string.append(t.CONSTANTS[token])
            continue
        if token in t.FUNCTIONS:
            stack.append(token)
            continue
        if token == t.FUNC_DELIMITER:
            while stack[-1] != t.O_BRACKET:
                output_string += [stack.pop()]
                if not stack:
                    raise exeptions.BracketsError('brackets are not balanced')
            continue
        if token in t.OPERATORS:
            while stack[-1] in t.OPERATORS and \
                    ((token in t.LEFT_ASSOCIATIVITY and t.OPERATORS[token].priority <= t.OPERATORS[
                        stack[-1]].priority) or
                     (token in t.RIGHT_ASSOCIATIVITY and t.OPERATORS[token].priority < t.OPERATORS[
                         stack[-1]].priority)):
                output_string += [stack.pop()]
                continue
            stack.append(token)
            continue
        if token == t.O_BRACKET:
            stack.append(token)
            continue
        if token == t.C_BRACKET:
            while stack[-1] != t.O_BRACKET:
                output_string += [stack.pop()]
                if not stack:
                    raise exeptions.BracketsError('brackets are not balanced')
            stack.pop()
            if stack[-1] in t.FUNCTIONS:
                output_string += [stack.pop()]
            continue
        raise exeptions.UnknownFunctionError(f'unknown function \'{token}\'')
    while stack[-1]:
        if stack[-1] == t.O_BRACKET:
            raise exeptions.BracketsError('brackets are not balanced')
        if stack[-1] in t.OPERATORS:
            output_string += [stack.pop()]
    return output_string


def make_valid(expression):
    """Call all validation functions and return valid string"""
    expression = dell_spaces(expression)
    expression = make_unarys(expression)
    chek_invalid_func(expression)
    return expression


def is_number(token):
    """Check if token is number"""
    return token.isdigit() or is_float(token)


def is_float(token):
    """Check if token is float"""
    try:
        float(token)
        return True
    except ValueError:
        return False


def make_unarys(infix_string):
    """Translate unary operators in list

    into they analogs"""
    output_string = list()
    for index, token in enumerate(infix_string):
        last_token = infix_string[index - 1]
        if token in t.OPERATORS and token in ('+', '-') and is_unary(infix_string, index):
            if token == '+':
                output_string.append('#')
            elif token == '-':
                output_string.append('~')
        else:
            output_string.append(token)
    return output_string


def is_unary(tokens, index):
    """Check if operator in tokens with index is unary"""
    token = tokens[index - 1]
    if token == ' ':
        token = tokens[index - 2]
    return (token in t.OPERATORS or
            token in t.FUNCTIONS or
            token == t.FUNC_DELIMITER or
            not index or
            token == t.O_BRACKET)


def chek_invalid_func(tokens):
    """Check for all func tokens valid"""
    for index, token in enumerate(tokens):
        if token in t.FUNCTIONS:
            if len(tokens) <= 1:
                raise exeptions.InvalidStringError('invalid string')
            if is_number(tokens[index + 1]):
                raise exeptions.InvalidStringError('invalid string')


def dell_spaces(tokens):
    """Delete all space tokens"""
    no_spaces_tokens = []
    for index, token in enumerate(tokens):
        if token == ' ':
            if is_number(tokens[index - 1]) and is_number(tokens[index + 1]):
                raise exeptions.InvalidStringError('invalid string')
        else:
            no_spaces_tokens.append(token)
    return no_spaces_tokens
