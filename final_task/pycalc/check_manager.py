import sys
from .operator_manager import operator_dict, function_dict


def check_expression(expression_line):
    if not expression_line:
        raise SyntaxError('Expression cannot be empty')
    if expression_line.count('(') < expression_line.count(')'):
        raise SyntaxError('Opening bracket required!')
    elif expression_line.count('(') > expression_line.count(')'):
        raise SyntaxError('Closing bracket required!')
    return expression_line


def check_parsing_list(parsing_list):
    if parsing_list[0] in operator_dict.keys():
        if parsing_list[0] is not '+' and parsing_list[0] is not '-':
            raise SyntaxError('Expression cannot start with "{}"'.format(parsing_list[0]))
    if len(parsing_list) == 1:
        if isinstance(parsing_list[0], int) or isinstance(parsing_list[0], float):
            return parsing_list
        raise SyntaxError('Expression must include at list one operand!')
    if parsing_list[-1] in operator_dict.keys():
        raise SyntaxError('Extra operator "{}" at the end of an expression!'.format(parsing_list[-1]))
    if parsing_list[-1] in function_dict.keys():
        raise SyntaxError('Function "{}" without argument'.format(parsing_list[-1]))
    return parsing_list


def operator_check(operator_symbol):
    if operator_symbol in operator_dict.keys():
        return operator_symbol
    raise SyntaxError('Typo in math operator!')


def number_check(number):
    try:
        return int(number)
    except ValueError:
        return float(number)


def function_check(function_name):
    if function_name == 'e' or function_name == 'pi':
        return function_dict[function_name]['operator']
    elif function_name == 'tau':
        if sys.version_info >= (3, 6):
            return function_dict[function_name]['operator']
        else:
            return 2 * function_dict['pi']['operator']
    elif function_name in function_dict.keys():
        return function_name
    else:
        raise SyntaxError(
            'There is no function with this name {}!'.format(function_name)
        )
