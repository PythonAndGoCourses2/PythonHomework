import argparse


def parse_console():
    """Parse args from console and returns it"""
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    return parser.parse_args().EXPRESSION
