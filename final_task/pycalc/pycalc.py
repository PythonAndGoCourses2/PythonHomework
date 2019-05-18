#!/usr/bin/python3

from .calculator import Calculator
from .argument_parser import arg_parser


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
