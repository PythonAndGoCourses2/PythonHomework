"""Check manager module"""

import sys
from .operator_manager import operator_dict


def check_expression(expression_line):
    """
    Check if the expression_line is not empty and the brackets are correct,
    otherwise raise an Exception
    :param expression_line: string from the user
    :return: clear expression line as str
    """
    if not expression_line:
        raise SyntaxError('Expression cannot be empty')
    if expression_line.count('(') < expression_line.count(')'):
        raise SyntaxError('Opening bracket required!')
    elif expression_line.count('(') > expression_line.count(')'):
        raise SyntaxError('Closing bracket required!')
    return expression_line


def check_parsing_list(parsing_list, function_dict):
    """
    Check if the parsing list is valid otherwise raise an Exception for next reasons:
    - expression starts with math operators (except "+" and "-")
    - there is no operand in the expression line
    - expression line ends with math operator or math function
    :param parsing_list: list from instance of SplitOperators class
    :param function_dict: dict with all functions {'operator': function, 'priority': 0}
    :return: clear parsing_list as str
    """
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
    """
    Check if there is an operator with this symbol in the operators_dict
    :param operator_symbol: last_symbol (str) from instance of SplitOperators class
    :return: clear operator_symbol as str
    """
    if operator_symbol in operator_dict.keys():
        return operator_symbol
    raise SyntaxError('Typo in math operator!')


def number_check(number):
    """
    Check if number is int or float
    :param number: last_number (str) from instance of SplitOperators class
    :return: number as int or float
    """
    try:
        return int(number)
    except ValueError:
        return float(number)


def function_check(function_name, function_dict):
    """
    Check if function_name is a key in function_dict.
    Check the python version to add constant "tau".
    If function_name is "pi", "e", "tau", "inf" or "nan" convert it into float
    If there is no such name in function_dict Raise an Exception
    :param function_name: last_letter (str) from instance of SplitOperators class
    :param function_dict: dict with all functions {'operator': function, 'priority': 0}
    :return: float or clear function_name as str
    """
    if function_name == 'tau':
        if sys.version_info >= (3, 6):
            return function_dict[function_name]['operator']
        else:
            return 2 * function_dict['e']['operator']
    elif function_name in function_dict.keys():
        if isinstance(function_dict[function_name]['operator'], int) \
                or isinstance(function_dict[function_name]['operator'], float):
            return function_dict[function_name]['operator']
        return function_name
    else:
        raise SyntaxError(
            'There is no function with this name {}!'.format(function_name)
        )
