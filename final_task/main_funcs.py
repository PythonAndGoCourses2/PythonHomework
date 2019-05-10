"""

module which pack main logic functions into functions which more easier to understand

"""

import logic
import constants


def calc_init(user_imports=None)-> dict:
    """

    function gets methods of user packages and package math

    :param user_imports: list of strings which contains user import methods
    :return: methods of user packages and package math
    """
    try:
        if user_imports:
            constants.imports.extend(user_imports)
        available_units = logic.import_usr_imports(constants.imports)
        methods = logic.get_imports_attrs(constants.imports, available_units)
        return methods
    except Exception as ex:
        print('ERROR: {}\n'.format(ex))


def calculate(expression_str: str, methods=None) -> str:
    """
    :param expression_str: mathematical expression to calculate
    :param methods: methods of user packages and package math
    :return: result of calculation
    """
    try:
        normal_list = logic.str_parse(expression_str, methods)
        polish_list = logic.rebuild_into_polish_notation(normal_list, methods)
        calculation_result = logic.ex_calc(polish_list, methods)
        if isinstance(calculation_result, list) and len(calculation_result) > 1:
            raise Exception('check your expression looks like you forgot an operator')
        calc_result = str(calculation_result)
        calc_result = logic.check_for_scientific_notation(calc_result)
        return calc_result
    except Exception as ex:
        print('ERROR: {}\n'.format(ex))
