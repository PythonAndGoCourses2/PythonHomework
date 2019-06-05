import argparse
import sys
from .parser import parse_input_string
from .sorter import create_polish_notation
from .calculation import get_result
from . import constants


def main():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
    parser.add_argument('EXPRESSION', help='Input string to evaluate', type=str)
    parser.add_argument('-m', '--modules', help='Additional modules to use', type=str)
    args = parser.parse_args()
    try:
        if args.EXPRESSION:
            if args.modules:
                for item in args.modules:
                    __import__(item)
                    add_functions = dict([(attr, getattr(sys.modules[item], attr)) for attr in dir(sys.modules[item]) if
                                          callable(getattr(sys.modules[item], attr))])
                    constants.FUNCTIONS = {**constants.FUNCTIONS, **add_functions}
            tokens_in_infix = parse_input_string(args.EXPRESSION)
            tokens_in_polish = create_polish_notation(tokens_in_infix)
            print(get_result(tokens_in_polish))
        else:
            raise Exception
    except Exception:
        print('ERROR: Something went wrong')


if __name__ == '__main__':
    main()
