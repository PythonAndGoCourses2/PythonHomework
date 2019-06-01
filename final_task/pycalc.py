import argparse
from sys import argv

from pycalc_proc import PyCalcProcessing


def create_parser():
    parser_ = argparse.ArgumentParser(prog='Py Calc',
                                      description='Pure-python command-line calculator',
                                      epilog='(c) Alina Laevskaya 2019.'
                                      )

    parser_.add_argument('EXPRESSION', type=str, help='String formula for processing.')
    return parser_


def main():
    parser = create_parser()
    namespace = parser.parse_args(argv[1:])
    py_calc_obj = PyCalcProcessing(namespace.EXPRESSION)
    py_calc_obj.launch_processing()


if __name__ == '__main__':
    main()
