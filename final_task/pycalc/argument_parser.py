"""Argument parser module"""

import argparse


def arg_parser():
    """
    This function gather positional arguments from users
    :return: expression_line as str
    """
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.', prog='pycalc')
    parser.add_argument(
        '-m',
        '--use-modules',
        help='additional modules to use',
        metavar='MODULE [MODULE ...]'
    )
    parser.add_argument(
        'EXPRESSION', help='expression string to calculate'
    )
    expression_line = parser.parse_args().EXPRESSION
    return expression_line
