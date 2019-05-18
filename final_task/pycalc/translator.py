"""Module contains functions to translate infix notation into postfix"""
from pycalc import library as lib
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
        elif token in lib.CONSTANTS:
            output_string.append(lib.CONSTANTS[token])
        elif token in lib.FUNCTIONS:
            stack.append(token)
        elif token == lib.FUNC_DELIMITER:
            stack, output_string = process_func_delimiter(stack, output_string)
        elif token in lib.OPERATORS:
            stack, output_string = process_operator(token, stack, output_string)
        elif token == lib.OPEN_BRACKET:
            stack.append(token)
        elif token == lib.CLOSE_BRACKET:
            stack, output_string = process_close_bracket(stack, output_string)
        else:
            raise exeptions.UnknownFunctionError(f'unknown function \'{token}\'')
    while stack[-1]:
        if stack[-1] == lib.OPEN_BRACKET:
            raise exeptions.BracketsError('brackets are not balanced')
        if stack[-1] in lib.OPERATORS:
            output_string += [stack.pop()]
    return output_string


def process_func_delimiter(stack: list, output_string: str):
    """function to make func delimiter branch"""
    while stack[-1] != lib.OPEN_BRACKET:
        output_string += [stack.pop()]
        if not stack:
            raise exeptions.BracketsError('brackets are not balanced')
    return stack, output_string


def process_operator(token: str, stack: list, output_string: str):
    """function to make operator branch"""
    while stack[-1] in lib.OPERATORS and \
            ((token in lib.LEFT_ASSOCIATIVITY and lib.OPERATORS[token].priority <= lib.OPERATORS[
                stack[-1]].priority) or
             (token in lib.RIGHT_ASSOCIATIVITY and lib.OPERATORS[token].priority < lib.OPERATORS[
                 stack[-1]].priority)):
        output_string += [stack.pop()]
        continue
    stack.append(token)
    return stack, output_string


def process_close_bracket(stack: list, output_string: str):
    """function to make close bracket branch"""
    while stack[-1] != lib.OPEN_BRACKET:
        output_string += [stack.pop()]
        if not stack:
            raise exeptions.BracketsError('brackets are not balanced')
    stack.pop()
    if stack[-1] in lib.FUNCTIONS:
        output_string += [stack.pop()]
    return stack, output_string


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
        if token in lib.OPERATORS and token in ('+', '-') and is_unary(infix_string, index):
            if token == '+':
                output_string.append(lib.UNARY_PLUS)
            elif token == '-':
                output_string.append(lib.UNARY_MINUS)
        else:
            output_string.append(token)
    return output_string


def is_unary(tokens, index):
    """Check if operator in tokens with index is unary"""
    if not abs(index) in range(len(tokens)):
        raise exeptions.GeneralError(f'Invalid token index in translator.py/is_unary \'{index}\'')
    token = tokens[index - 1]
    if token == ' ':
        token = tokens[index - 2]
    return (token in lib.OPERATORS or
            token in lib.FUNCTIONS or
            token == lib.FUNC_DELIMITER or
            not index or
            token == lib.OPEN_BRACKET)


def chek_invalid_func(tokens):
    """Check for all func tokens valid"""
    for index, token in enumerate(tokens):
        if token in lib.FUNCTIONS:
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
