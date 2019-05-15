from . import operator_manager


def check_expression(expression_line):
    if not expression_line:
        raise SyntaxError('Expression cannot be empty')
    if expression_line.count('(') < expression_line.count(')'):
        raise SyntaxError('Opening bracket required!')
    elif expression_line.count('(') > expression_line.count(')'):
        raise SyntaxError('Closing bracket required!')
    return True