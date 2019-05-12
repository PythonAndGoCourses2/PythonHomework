# -*- coding: utf-8 -*-
"""
The module is designed to work with mathematical expressions.

Example:
        $ python pycalc.py -h
        $ python pycalc.py 'expretion'
        $ python pycalc.py 'expretion' -m 'module1' 'module2'
"""

import re
from library import Library
from parser import parse_query
from checker import check_expression
from replacer import replace_all_mathes
from regexp import has_comparator
from converter import convert_answer


def main():
    """Performs processing and calculation of the request from the command line and displays it on the screen."""
    try:
        lib = Library('math')
        args = parse_query()
        lib.update(*args.modules)
        expr = check_expression(args.expr, lib)
        has_compare = has_comparator(expr)
        answer = replace_all_mathes(expr, lib)
        answer = convert_answer(answer, has_compare)
        print(answer)
    except Exception as e:
        print(f'ERROR: {e}')


if __name__ == '__main__':
    main()
