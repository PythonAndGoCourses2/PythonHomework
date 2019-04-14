"""

module which contains class of calculator which will be used for easy calculating expression

"""

import logic
import constants
import pycodestyle
from typing import Any

pycodestyle.maximum_line_length = 120


class PyCalc:

    def __init__(self, user_imports=[]):
        try:
            constants.imports.extend(user_imports)
            logic.import_usr_imports(constants.imports)
            self._methods = logic.get_imports_attrs(constants.imports)
        except Exception as ex:
            print('Error: {}\n'.format(ex))

    def calculate(self, expression_str: str) -> Any:
        try:
            normal_list = logic.str_parse(expression_str)
            polish_list = logic.polish_notation(normal_list, self._methods)
            return logic.ex_calc(polish_list, self._methods)
        except Exception as ex:
            print('Error: {}\n'.format(ex))
