from .operator_manager import operator_dict, function_dict, unary_dict


def check_expression(parsing_list):
    if not parsing_list:
        raise SyntaxError('Expression cannot be empty')
    if parsing_list.count('(') < parsing_list.count(')'):
        raise SyntaxError('Opening bracket required!')
    elif parsing_list.count('(') > parsing_list.count(')'):
        raise SyntaxError('Closing bracket required!')
    if parsing_list[0] in operator_dict.keys():
        if parsing_list[0] is not '+' and parsing_list[0] is not '-':
            raise SyntaxError('Expression cannot start with "{}"'.format(parsing_list[0]))
    if len(parsing_list) == 1:
        if type(parsing_list[0]) is int or type(parsing_list[0]) is float:
            return True
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
            return 2 * function_dict['e']['operator']
    elif function_name in function_dict.keys():
        return function_name
    else:
        raise SyntaxError(
            'There is no function with this name {}!'.format(function_name)
        )
