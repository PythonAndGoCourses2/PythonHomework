import argparse
from . import parse_input_expression
from . import create_polish_notation
from . import calculate


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
            print(calculate(tokens_in_polish))
        else:
            raise Exception('EXPRESSION is empty')
    except Exception as error:
        print("ERROR: " + str(error))


if __name__ == '__main__':
    main()
