#!/usr/bin/python3

import argparse
from .calculator import Calculator


def arg_parser():
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


def main():
    try:
        expression_line = arg_parser()
        calc = Calculator(expression_line)
        result = calc.calculate()
        print(result)
    except SyntaxError as err:
        print('ERROR: {}'.format(err))
    except ZeroDivisionError as err:
        print('ERROR: {}!'.format(err))
    except ValueError as err:
        print('ERROR: {}!'.format(err))
    except OverflowError as err:
        print('ERROR: {}!'.format(err))


if __name__ == '__main__':
    main()
