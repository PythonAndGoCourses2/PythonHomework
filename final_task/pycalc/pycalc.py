#!/usr/bin/python3
"""pycalc module"""

from .calculator import Calculator
from .argument_parser import arg_parser


def main():
    """
    This function take expression_line from users and invokes calculation. Wrapped in try block to catch error
    messages while preparing expression and calculating itself
    :return: result of calculation of the users expression
    """
    try:
        expression_line = arg_parser()
        calc = Calculator(expression_line.expression, expression_line.functions)
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
