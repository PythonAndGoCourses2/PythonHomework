import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
    # specify which command-line options the program is willing to accept
    parser.add_argument('EXPRESSION', help='expression string to evaluate',)
    # return data from EXPRESSION
    args = parser.parse_args()
    expression = args.EXPRESSION
    return expression
