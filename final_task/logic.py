import re
import inspect
import importlib
import constants
import pycodestyle
from typing import Any

pycodestyle.maximum_line_length = 120


def import_usr_imports(usr_imports: list):
    """import user files

    function gets objects of user imports and added it to global namespace

    :param usr_imports: bunch of user imports names
    :return: nothing
    """
    import_objects = dict()

    for import_elem in usr_imports:
        import_objects[import_elem] = importlib.import_module(import_elem)

    globals().update(import_objects)


def _get_item_by_type(item: str, methods: dict) -> Any:
    """get item by its string according its type

    :param item: string of equivalent of some number
    :param methods: dictionary which contains objects of methods of imports
    :return: number by its type
    """
    if not type(item) is str:
        return item
    if constants.RE_FLOATS.findall(item):
        return float(item)
    elif constants.RE_INTS.findall(item):
        return int(item)
    elif constants.RE_FUNCTIONS.findall(item) and not callable(methods[item]):
        return methods[item]
    else:
        return None


def get_imports_attrs(user_imports: list) -> dict:
    """get methods of user imports as dictionary

    :param user_imports: list of names of user imports
    :return: dictionary which contains names of methods of imports as keys and its object as values
    """
    output_dict = dict()
    for element in user_imports:
        output_dict.update(_get_unit_attrs(element))
    return output_dict


def _get_unit_attrs(unit: str) -> dict:
    """get attributes of unit by it name

    :param unit: name of unit as string
    :return: dictionary which contains name of attribute as key and it object as value
    """
    attrs = tuple([i for i in dir(globals()[unit])])
    output_dict = dict()
    for attribute in attrs:
        if not attribute.count('_'):
            output_dict[attribute] = getattr(globals()[unit], attribute)
    return output_dict


def str_parse(ex_str: str) -> list:
    """parse mathematical expression string using regular expressions

    :param ex_str: expression string
    :return: list made of parsed expression string
    """
    if ex_str.count('(') != ex_str.count(')'):
        raise Exception('brackets are not balanced')

    expression = re.compile(r'[+\-*%^()]|[0-9]+[.][0-9]+|[0-9a-zA-Z]+|[a-zA-Z]+|[/<=!>]+|[0-9]+')
    negative = re.compile(r'[^0-9)a-zA-Z][\-][0-9]+|[^0-9)a-zA-Z][\-][a-zA-Z]+')
    positive = re.compile(r'[^0-9)a-zA-Z][+][0-9]+|[^0-9)a-zA-Z][+][a-zA-Z]+')
    float_val = re.compile(r'[^0-9][.][0-9]+')
    start_string_float_val = re.compile(r'^[.][0-9]+')
    extra_operators = re.compile(r'[+\-]{2,}')
    start_of_string_operator = re.compile(r'^[+\-][0-9]+[.][0-9]+|^[+\-][0-9]+|^[+\-][a-zA-Z]+')

    ex_str = ex_str.replace('--', '+')

    if start_string_float_val.findall(ex_str):
            ex_str = ex_str.replace(ex_str, '0' + ex_str)

    while float_val.findall(ex_str):
        for element in float_val.findall(ex_str):
            ex_str = ex_str.replace(element, element[0:1] + '0' + element[1:])

    while negative.findall(ex_str):
        for element in negative.findall(ex_str):
            ex_str = ex_str.replace(element, element[0:1] + '0' + element[1:])

    while negative.findall(ex_str):
        for element in negative.findall(ex_str):
            ex_str = ex_str.replace(element, element[0:1] + '0' + element[1:])

    while positive.findall(ex_str):
        for element in positive.findall(ex_str):
            ex_str = ex_str.replace(element, element[0:1] + '0' + element[1:])

    while extra_operators.findall(ex_str):
        while negative.findall(ex_str):
            for element in negative.findall(ex_str):
                ex_str = ex_str.replace(element, element[0:1] + '0' + element[1:])

        while positive.findall(ex_str):
            for element in positive.findall(ex_str):
                ex_str = ex_str.replace(element, element[0:1] + '0' + element[1:])

    if start_of_string_operator.findall(ex_str):
        ex_str = ex_str.replace(ex_str, '0' + ex_str)

    return expression.findall(ex_str)


def _priority(expression: str) -> int:
    """evaluate priority of given mathematical operator

    :param expression: mathematical operator
    :return: priority of given operator as integer
    """
    if expression == constants.lowest_priority_operator:
        return constants.LOWEST_PRIORITY
    elif expression in constants.low_priority_operators:
        return constants.LOW_PRIORITY
    elif expression in constants.mid_priority_operators:
        return constants.MID_PRIORITY
    elif expression in constants.high_priority_operators:
        return constants.HIGH_PRIORITY
    elif expression == constants.highest_priority_operator:
        return constants.HIGHEST_PRIORITY
    else:
        return -1


def polish_notation(expression_list: list, methods: dict) -> list:
    """rewrite mathematical expression list into polish notation

    :param expression_list: parsed list of mathematical expression
    :param methods: dictionary which contains name of attribute as key and it object as value
    :return: rewrited into polish notation list of mathematical expression
    """
    output_expression = []
    operation_list = []

    for expression in expression_list:
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
                and not constants.RE_FUNCTIONS.findall(expression) :
            # if we found number
            output_expression.append(expression)
            continue

        if constants.RE_OPERATIONS.findall(expression)or(constants.RE_FUNCTIONS.findall(expression)
                                                         and not callable(methods[expression])):
            if (not operation_list or _priority(expression) > _priority(operation_list[-1])) and expression != '(':
                # if we found operator or function and it priority higher than priority of operator on the top of
                # operators stack add it into operators stack
                operation_list.append(expression)

            elif operation_list and _priority(operation_list[-1]) >= _priority(expression):
                # if we found operator and it priority lower than priority of operator on the top of
                # operators stack pop all of operators in operators stack into output stack
                while operation_list and _priority(operation_list[-1]) >= _priority(expression):
                    if expression == '(':
                        break
                    output_expression.append(operation_list.pop())

                if expression != '(':
                    operation_list.append(expression)

        if expression == '(':
            operation_list.append(expression)

        if expression == ')':
            while operation_list[-1] != '(':
                if operation_list:
                    output_expression.append(operation_list.pop())
            operation_list.pop()
            if operation_list and constants.RE_FUNCTIONS.findall(operation_list[-1]):
                # if after '(' we found operation also push it into output list
                output_expression.append(operation_list.pop())

    while operation_list:
        output_expression.append(operation_list.pop())

    return output_expression


def ex_calc(polish_list: list, methods: dict) -> float:
    """calculate mathematical expression writed as polish notation

    :param polish_list: list which contains mathematical expression writed as polish notation
    :param methods: dictionary which contains manes of methods of user imports as keys and objects of it as values
    :return: result of calculated mathematical expression
    """
    output_list = []
    for ex in polish_list:
        if constants.RE_FLOATS.findall(ex) or constants.RE_INTS.findall(ex) and not constants.RE_FUNCTIONS.findall(ex):
            output_list.append(ex)
            continue

        if constants.RE_FUNCTIONS.findall(ex):
            values = []

            if not callable(methods[ex]):  # if word is constant value just write it into output list
                output_list.append(methods[ex])
                continue

            signature = inspect.signature(methods[ex])
            parameters_count = len(signature.parameters)
            parameters = signature.parameters
            for parameter in parameters:  # get count of parameters of function
                if not parameters[parameter].default:
                    parameters_count -= 1
            while parameters_count > 0:
                if output_list:
                    float_val = float(output_list.pop())
                    values.append(float_val)
                parameters_count -= 1

            # perform mathematical function and write result into output List
            output_list.append(methods[ex](*values[::-1]))

        if constants.RE_OPERATIONS.findall(ex):  # if found operation perform it
            second_val = _get_item_by_type(output_list.pop(), methods)
            first_val = _get_item_by_type(output_list.pop(), methods)
            output_list.append(constants.operator[ex](first_val, second_val))

    return _get_item_by_type(output_list[0], methods)

# goals for weekend

# argparse (!!!)
# setuptools(!!!)

