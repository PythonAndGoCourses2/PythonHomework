import argparse
from .parser import parse_input_string
from .sorter import create_polish_notation
from .calculation import get_result


def create_parser():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
    parser.add_argument('EXPRESSION', help='Input string to evaluate',)
    args = parser.parse_args()
    input_string = args.EXPRESSION
    return input_string


def main():
    try:
        input_string = create_parser()
        if input_string:
            tokens_in_infix = parse_input_string(input_string)
            tokens_in_polish = create_polish_notation(tokens_in_infix)
            print(get_result(tokens_in_polish))
        else:
            raise Exception
    except Exception:
        print('ERROR: Something went wrong')


if __name__ == '__main__':
    main()
