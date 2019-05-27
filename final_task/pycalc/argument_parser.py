"""Argument parser module"""

import argparse
from collections import namedtuple
from .operator_manager import create_func_dict, find_user_functions


def arg_parser():
    """
    This function gather positional arguments from users,
    create a function_dict with users and built_in math functions if there is users_modules,
    esle create a function_dict only with built_in math functions
    :return: line as namedtuple(expression, function_dict)
    """
    parser = argparse.ArgumentParser(
                                    description='Pure-python command-line calculator.',
                                    prog='pycalc_not_my'
                                    )
    parser.add_argument(
                        '-m',
                        '--use-modules',
                        help='additional modules to use',
                        metavar='MODULE [MODULE ...]'
                        )
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    args = parser.parse_args()
    expression = args.EXPRESSION
    if args.use_modules:
        user_functions = find_user_functions(args.use_modules)
        function_dict = create_func_dict(user_functions)
        expression_line = namedtuple('expression_line', 'expression functions')
        line = expression_line(expression, function_dict)
    else:
        function_dict = create_func_dict()
        expression_line = namedtuple('expression_line', 'expression functions')
        line = expression_line(expression, function_dict)
    return line
