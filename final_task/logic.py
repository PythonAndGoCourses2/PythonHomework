"""

module which contains methods which make up base logic of the calculator

"""
import re
import importlib
import constants
from typing import Any


def parse_funcs_params(ex_list: list, methods: dict) -> list:
    """

    function which write function parameters into list, its work recursively if find another function in one of
    parameters

    :param ex_list: list which contains mathematical expression
    :param methods: methods which available for user
    :return: rewrited list
    """
    if not ex_list:
        return []
    brackets_count = 0
    found_func = False
    output_list = list()
    params_list = list()
    params_buff_list = list()
    one_param_list = list()
    for ex in ex_list:
        if constants.RE_FUNCTIONS.findall(ex) and callable(methods[ex]):
            if not found_func:
                found_func = True
                output_list.append(ex)
            else:
                one_param_list.append(ex)
            continue
        if ex == '(':
            if found_func:
                if output_list and constants.RE_FUNCTIONS.findall(output_list[-1]):
                    output_list.append(ex)
                else:
                    one_param_list.append(ex)
                brackets_count += 1
            else:
                output_list.append(ex)
            continue
        if ex == ')' and brackets_count:
            brackets_count -= 1
            if not brackets_count:
                found_func = False
                params_list.append(one_param_list)
                one_param_list = []
                for param_list in params_list:
                    params_buff_list.append(parse_funcs_params(param_list, methods))
                params_list = params_buff_list
                output_list.append(params_list)
                params_list = []
                params_buff_list = []
                output_list.append(ex)
            else:
                one_param_list.append(ex)
            continue
        if ex == ',' and brackets_count == 1:
            params_list.append(one_param_list)
            one_param_list = []
            continue
        if brackets_count and found_func:
            one_param_list.append(ex)
            continue
        output_list.append(ex)

    return output_list


def import_usr_imports(usr_imports: list):
    """import user files

    function gets objects of user imports and added it to global namespace

    :param usr_imports: bunch of user imports names
    :return: nothing
    """
    import_objects = {import_elem: importlib.import_module(import_elem) for import_elem in usr_imports}
    return import_objects


def _get_item_by_type(item: str, methods: dict) -> Any:
    """get item by its string according its type

    :param item: string of equivalent of some number
    :param methods: dictionary which contains objects of methods of imports
    :return: number by its type
    """
    if not isinstance(item, str):
        return item
    if constants.RE_FLOATS.findall(item):
        output_value = float(item)
    elif constants.RE_INTS.findall(item):
        output_value = int(item)
    elif constants.RE_FUNCTIONS.findall(item) and not callable(methods[item]):
        output_value = methods[item]
    else:
        output_value = None

    return output_value


def get_imports_attrs(user_imports: list, available_units: dict) -> dict:
    """get methods of user imports as dictionary

    :param available_units: units which contains functions and constants which user can use
    :param user_imports: list of names of user imports
    :return: dictionary which contains names of methods of imports as keys and its object as values
    """
    output_dict = dict()
    for element in user_imports:
        output_dict.update(_get_unit_attrs(element, available_units))
    output_dict.update(constants.builtin_funcs_dict)
    return output_dict


def _get_unit_attrs(unit: str, available_units: dict) -> dict:
    """get attributes of unit by it name

    :param unit: name of unit as string
    :return: dictionary which contains name of attribute as key and it object as value
    """
    attrs = tuple(i for i in dir(available_units[unit]))
    output_dict = dict()
    for attribute in attrs:
        if not attribute.count('_'):
            output_dict[attribute] = getattr(available_units[unit], attribute)
    return output_dict


def str_parse(ex_str: str, methods: dict) -> list:
    """parse mathematical expression string using regular expressions

    :param methods: dictionary of available methods for user
    :param ex_str: expression string
    :return: list made of parsed expression string
    """
    re_paired_operators = re.compile(r'[+][-]|[-][+]')
    re_multiple_minuses = re.compile(r'[\-]{2,}')
    re_multiple_pluses = re.compile(r'[+]{2,}')
    re_function = re.compile(r'[a-zA-Z]+')

    error_handle(ex_str, methods)

    ex_str = ex_str.replace(' ', '')

    for match in constants.RE_INCOMPLETE_FLOAT.findall(ex_str):
        ex_str = ex_str.replace(match, match[0] + '0' + match[1:])

    for match in constants.RE_NEGATIVE_CONSTANTS.findall(ex_str):
        if not callable(methods[match[2:]]):
            ex_str = ex_str.replace(match, match[0] + '(0' + match[1:] + ')')

    while re_paired_operators.findall(ex_str):
        for operators in re_paired_operators.findall(ex_str):
            ex_str = ex_str.replace(operators, '-')
            if not ex_str.count(operators):
                break

    while constants.RE_NEGATIVE_FUNCS.findall(ex_str):
        for negative_func in constants.RE_NEGATIVE_FUNCS.findall(ex_str):
            negative_func_start_index = ex_str.find(negative_func) + 1
            all_func = _find_negative_func(ex_str, negative_func_start_index)
            ex_str = ex_str.replace(all_func, '(0' + all_func + ')')
            continue

    if constants.RE_NEGATIVE_VALUES_ON_STR_BEG.findall(ex_str):
        ex_str = '0' + ex_str

    for negative_value in constants.RE_NEGATIVE_VALUES.findall(ex_str):
        if re_function.findall(negative_value) and \
                callable(methods[re_function.findall(negative_value)[0]]):
            continue
        ex_str = ex_str.replace(negative_value, negative_value[0] + '(0' + negative_value[1:] + ')')

    while re_multiple_minuses.findall(ex_str) or re_multiple_pluses.findall(ex_str):
        for minuses in re_multiple_minuses.findall(ex_str):
            if minuses.count('-') % 2 == 0:
                ex_str = ex_str.replace(minuses, '+')
            elif minuses.count('-') % 2 != 0:
                ex_str = ex_str.replace(minuses, '-')
        for pluses in re_multiple_pluses.findall(ex_str):
            ex_str = ex_str.replace(pluses, '+')

    parse_list = constants.RE_MAIN_PARSE_ARG.findall(ex_str)

    packed_expression = parse_funcs_params(parse_list, methods)

    return packed_expression


def _get_priority(expression: str) -> int:
    """evaluate priority of given mathematical operator

    :param expression: mathematical operator
    :return: priority of given operator as integer
    """
    if expression in constants.operations_priority_dict.keys():
        return constants.operations_priority_dict[expression]
    else:
        return -1


def rebuild_into_polish_notation(expression_list: list, methods: dict) -> list:
    """rewrite mathematical expression list into polish notation

    :param expression_list: parsed list of mathematical expression
    :param methods: dictionary which contains name of attribute as key and it object as value
    :return: rewrited into polish notation list of mathematical expression
    """
    output_expression = []
    operation_list = []

    for expression in expression_list:
        if isinstance(expression, list):
            output_expression.append(rebuild_into_polish_notation(expression, methods))
            continue
        if constants.RE_FUNCTIONS.findall(expression) and expression not in methods.keys():
            raise Exception('unknown function {}'.format(expression))
        if constants.RE_FUNCTIONS.findall(expression) and not callable(methods[expression]):
            # if we found constant value
            output_expression.append(expression)
            continue
        elif constants.RE_FUNCTIONS.findall(expression) and callable(methods[expression]):
            # if we found mathematical operation
            operation_list.append(expression)

        if constants.RE_FLOATS.findall(expression) or constants.RE_INTS.findall(expression) \
                and not constants.RE_FUNCTIONS.findall(expression):
            # if we found number
            output_expression.append(expression)
            continue

        if constants.RE_OPERATIONS.findall(expression) or (constants.RE_FUNCTIONS.findall(expression)
                                                           and not callable(methods[expression])):
            operation_list, output_expression = _check_for_operation_priority(operation_list, output_expression,
                                                                              expression)

        if expression == '(':
            operation_list.append(expression)

        if expression == ')':
            operation_list, output_expression = _push_operations_while_bracket(operation_list, output_expression)

    while operation_list:
        output_expression.append(operation_list.pop())

    return output_expression


def _push_operations_while_bracket(operation_list: list, polish_list: list) -> tuple:
    while operation_list[-1] != '(':
        if operation_list:
            polish_list.append(operation_list.pop())
    operation_list.pop()
    if operation_list and constants.RE_FUNCTIONS.findall(operation_list[-1]):
        # if after '(' we found operation also push it into output list
        polish_list.append(operation_list.pop())

    return operation_list, polish_list


def _check_for_operation_priority(operation_list: list, polish_list: list, expression: str):
    if (not operation_list or _get_priority(expression) > _get_priority(operation_list[-1])) and expression != '(':
        # if we found operator or function and it's priority higher than priority of operator on the top of
        # stack of operators add it into stack of operators
        operation_list.append(expression)

    elif operation_list and _get_priority(operation_list[-1]) >= _get_priority(expression):
        if operation_list and (expression == '^' and operation_list[-1] == '^'):
            operation_list.append(expression)
            return operation_list, polish_list
        # if we found operator and it priority lower than priority of operator on the top of
        # operators stack pop all of operators in operators stack into output stack
        while operation_list and _get_priority(operation_list[-1]) >= _get_priority(expression):
            if expression == '(':
                break
            polish_list.append(operation_list.pop())

        if expression != '(':
            operation_list.append(expression)

    return operation_list, polish_list


def ex_calc(polish_list: list, methods: dict) -> Any:
    """calculate mathematical expression writed as polish notation

    :param polish_list: list which contains mathematical expression writed as polish notation
    :param methods: dictionary which contains manes of methods of user imports as keys and objects of it as values
    :return: result of calculated mathematical expression
    """
    output_list = []
    for ex in polish_list:
        if isinstance(ex, list):
            output_list.append(ex_calc(ex, methods))
            continue
        if constants.RE_FLOATS.findall(ex) or constants.RE_INTS.findall(ex) and not constants.RE_FUNCTIONS.findall(ex):
            output_list.append(ex)
            continue

        if constants.RE_FUNCTIONS.findall(ex):
            if not callable(methods[ex]):  # if word is constant value just write it into output list
                output_list.append(methods[ex])
                continue
            else:
                if isinstance(output_list[-1], list):
                    output_list.append(methods[ex](*output_list.pop()))
                else:
                    output_list.append(methods[ex](output_list.pop()))
                continue

        if constants.RE_OPERATIONS.findall(ex):  # if found operation perform it
            second_val = _get_item_by_type(output_list.pop(), methods)
            first_val = _get_item_by_type(output_list.pop(), methods)
            output_list.append(constants.operators_methods_dict[ex](first_val, second_val))
            continue
    if len(output_list) > 1:
        return output_list
    else:
        return _get_item_by_type(output_list[0], methods)


def _find_negative_func(ex_str: str, func_index: int) -> str:
    last_bracket_index = func_index
    first_bracket_found = False
    brackets_count = 0
    for char in ex_str[func_index:]:
        last_bracket_index += 1
        if char == '(':
            if not first_bracket_found:
                first_bracket_found = True
            brackets_count += 1
            continue
        if char == ')':
            brackets_count -= 1
            if not brackets_count:
                break
    return ex_str[func_index:last_bracket_index]


def check_for_scientific_notation(number_str: str) -> str:
    """

    convert scientific notation of float numbers into normal float

    :param number_str: scientific notation number as string
    :return: normal float number as string
    """
    e_index = number_str.find('e')
    if e_index >= 0 and number_str.find('+') >= 0:
        remove_number = int(constants.RE_INTS.findall(number_str[e_index:])[0])
        if '+' in number_str:
            number_str = number_str[:e_index]
            number_str = number_str.replace('.', '')
            number_str = number_str[:remove_number] + '.' + number_str[remove_number:]
            if number_str[-1] == '.':
                number_str = number_str + '0'
        elif '-' in number_str:
            number_str = number_str[:e_index]
            number_str = number_str.replace('.', '')
            nulls = ['0' for _ in range(remove_number - 1)]
            number_str = '0.' + ''.join(nulls) + number_str
    return number_str


def error_handle(ex_str: str, methods):
    re_calc_operations = re.compile(r'[+\-*/^%]+')
    re_bool_operations = re.compile(r'[=<>!]+')
    num_calc_operations = len(re_calc_operations.findall(ex_str))
    num_bool_operators = len(re_bool_operations.findall(ex_str))
    nums_count = len(constants.RE_INTS.findall(ex_str)) + len(constants.RE_FLOATS.findall(ex_str))
    if not constants.RE_FUNCTIONS.findall(ex_str):
        if num_calc_operations and nums_count > num_calc_operations + 1:
            raise Exception('looks like you forgot an operation or a number')
        if num_bool_operators and nums_count > num_bool_operators + 1 or nums_count < num_bool_operators + 1:
            raise Exception('looks like you forgot an operation or a number')
    if not ex_str:
        raise Exception('nothing to calculate')
    if ex_str.count('(') != ex_str.count(')'):
        raise Exception('brackets are not balanced')
    for item in constants.RE_FUNCTIONS.findall(ex_str):
        if item not in methods.keys():
            raise Exception('unknown function '+item+'()')
