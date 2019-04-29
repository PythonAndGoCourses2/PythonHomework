import argparse
import main_funcs
import pycodestyle


def main():
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.', prog='pycalc')
    parser.add_argument('EXPRESSION', action='store', type=str, help='expression string to evaluate')
    parser.add_argument('-m', '--MODULE', type=str, help='use modules MODULE [MODULE...] additional modules to use')
    arguments = parser.parse_args()
    if arguments.MODULE:
        arguments.MODULE = arguments.MODULE.replace(' ', '')
        arguments.MODULE = arguments.MODULE.split(',')
        methods = main_funcs.calc_init(arguments.MODULE)
    else:
        methods = main_funcs.calc_init()
    print(main_funcs.calculate(arguments.EXPRESSION, methods))


if __name__ == '__main__':
    main()
