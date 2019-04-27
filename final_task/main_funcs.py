"""

module which pack main logic functions into functions which more easier to understand

"""

import logic
import constants
import pycodestyle
from typing import Any


def calc_init(user_imports=None)-> dict:
    try:
        if user_imports:
            constants.imports.extend(user_imports)
        available_units = logic.import_usr_imports(constants.imports)
        methods = logic.get_imports_attrs(constants.imports, available_units)
        return methods
    except Exception as ex:
        print('ERROR: {}\n'.format(ex))


def calculate(expression_str: str, methods=None) -> Any:
    try:
        normal_list = logic.str_parse(expression_str, methods)
        polish_list = logic.rebuild_into_polish_notation(normal_list, methods)
        return logic.ex_calc(polish_list, methods)
    except Exception as ex:
        print('ERROR: {}\n'.format(ex))
