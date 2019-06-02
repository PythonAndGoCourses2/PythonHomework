"""Module contains functions to translate infix notation into postfix"""
from pycalc.library import Library as lib
from pycalc import exeptions


def get_postfix(infix_notation: list) -> list:
    """Translate infix notation into postfix

    Returns list of tokens"""
    infix_notation = make_valid(infix_notation)
    output_string = []
    stack = [0]
    for token in infix_notation:
        if is_number(token):
            output_string.append(float(token))
        elif token in lib.user_constants:
            output_string.append(lib.user_constants[token])
        elif token in lib.CONSTANTS:
            output_string.append(lib.CONSTANTS[token])
        elif token in (*lib.FUNCTIONS, *lib.user_functions):
            stack.append(token)
        elif token == lib.FUNC_DELIMITER:
            process_func_delimiter(stack, output_string)
        elif token in lib.OPERATORS:
            process_operator(token, stack, output_string)
        elif token == lib.OPEN_BRACKET:
            stack.append(token)
            if infix_notation[infix_notation.index(token) + 1] == lib.CLOSE_BRACKET:
                stack.append(lib.FILLER)
        elif token == lib.CLOSE_BRACKET:
            process_close_bracket(stack, output_string)
        elif token in lib.NOT_SUPPORTED:
            raise exeptions.InvalidStringError('Calculator doesn\'t support iterable objects(list, set, dict)')
        else:
            raise exeptions.UnknownFunctionError(f'unknown function \'{token}\'')
    process_all_left(stack, output_string)
    return output_string


def process_func_delimiter(stack: list, output_string: list):
    """function to make func delimiter branch"""
    while stack[-1] != lib.OPEN_BRACKET:
        output_string += [stack.pop()]
        if not stack:
            raise exeptions.BracketsError('brackets are not balanced')
    output_string += ','


def process_operator(token: str, stack: list, output_string: list):
    """function to make operator branch"""
    while stack[-1] in lib.OPERATORS and \
            ((token in lib.LEFT_ASSOCIATIVITY and lib.OPERATORS[token].priority <= lib.OPERATORS[
                stack[-1]].priority) or
             (token in lib.RIGHT_ASSOCIATIVITY and lib.OPERATORS[token].priority < lib.OPERATORS[
                 stack[-1]].priority)):
        output_string += [stack.pop()]
        continue
    stack.append(token)


def process_close_bracket(stack: list, output_string: list):
    """function to make close bracket branch"""
    while stack[-1] != lib.OPEN_BRACKET:
        output_string += [stack.pop()]
        if not stack:
            raise exeptions.BracketsError('brackets are not balanced')
    stack.pop()
    if stack[-1] in lib.FUNCTIONS or stack[-1] in lib.user_functions:
        output_string += [stack.pop()]


def process_all_left(stack, output_string):
    """Pop all operators to the output string"""
    while stack[-1]:
        if stack[-1] == lib.OPEN_BRACKET:
            raise exeptions.BracketsError('brackets are not balanced')
        if stack[-1] in lib.OPERATORS:
            output_string += [stack.pop()]


def make_valid(expression):
    """Call all validation functions and return valid string"""
    expression = dell_spaces(expression)
    expression = make_unarys(expression)
    chek_invalid_func(expression)
    return expression


def is_number(token):
    return token.isdigit() or is_float(token)


def is_float(token):
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
    return (token in (*lib.OPERATORS,
                      *lib.FUNCTIONS,
                      *lib.user_functions,
                      *lib.FUNC_DELIMITER) or
            not index or
            token == lib.OPEN_BRACKET)


def chek_invalid_func(tokens):
    """Check for all func tokens valid"""
    for index, token in enumerate(tokens):
        if token in (*lib.FUNCTIONS, *lib.user_functions):
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
