import argparse
from .parser import parse_input_expression
from .sorter import create_polish_notation
from .calculation import get_result


def create_parser():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
    parser.add_argument('EXPRESSION', help='expression string to evaluate',)
    args = parser.parse_args()
    expression = args.EXPRESSION
    return expression


def main():
    try:
        expression = create_parser()
        if expression:
            tokens_in_infix = parse_input_expression(expression)
            tokens_in_polish = create_polish_notation(tokens_in_infix)
            print(get_result(tokens_in_polish))
        else:
            raise Exception
    except:
        print('ERROR: Something went wrong')


if __name__ == '__main__':
    main()
