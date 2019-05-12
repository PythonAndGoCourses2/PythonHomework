import argparse
from . import Exeptions


def parse_console():
    """Parse args from console and returns it"""
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    if parser.parse_args().EXPRESSION:
        return parser.parse_args().EXPRESSION
    else:
        raise Exeptions.GeneralError()
    # try:
    #     if parser.parse_args().EXPRESSION:
    #         return parser.parse_args().EXPRESSION
    #     else:
    #         raise Exeptions.GeneralError()
    # except Exeptions.GeneralError:
    #     print('ERROR: empty input')
    #     exit(1)
