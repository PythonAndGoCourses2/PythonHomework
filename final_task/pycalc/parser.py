"""Module to parse console args into string"""
import argparse
from pycalc import exeptions


def parse_arguments():
    """Parse args from console and returns it"""
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    parser.add_argument('-m', '--use_modules', nargs='*', metavar='MODULE', help='additional modules to use')
    if parser.parse_args().EXPRESSION:
        if parser.parse_args().use_modules:
            return parser.parse_args().module, parser.parse_args().EXPRESSION
        return parser.parse_args().EXPRESSION
    raise exeptions.GeneralError('empty string')
