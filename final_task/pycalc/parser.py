"""Module to parse console args into string"""
import argparse
from . import exeptions


def parse_console():
    """Parse args from console and returns it"""
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    # parser.add_argument('-m', '--use-modules', metavar='MODULE [MODULE ...]',type=list, help='additional modules to use')
    # print(parser.parse_args())
    if parser.parse_args().EXPRESSION:
        return parser.parse_args().EXPRESSION
    else:
        raise exeptions.GeneralError()
