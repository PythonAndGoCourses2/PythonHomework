#!/usr/bin/env python3

"""
The module contains functions for args parsing.
Use argument_parser.parse().
"""


import argparse
import sys


class ArgumentParserError(Exception):
    pass


class __ArgumentParser(argparse.ArgumentParser):
    """
    Overrides original exception-type to exception-type with human-readable error explanation.
    Write "ERROR: <message>" in stdout. Then return exit code 2.
    """
    def error(self, message):
        raise ArgumentParserError(message)


def parse():
    """Parse args from CLI and return a tuple: (expression: str, (modules: str): tuple)."""
    parser = __ArgumentParser(prog="pycalc", description="Pure-python command-line calculator.",
                              usage="pycalc [-h] EXPRESSION [-m MODULE [MODULE ...]]")

    if len(sys.argv) == 1:
        parser.print_usage()
        parser.exit()

    parser.add_argument(metavar="EXPRESSION",
                        type=str,
                        action="store",
                        dest="expression",
                        help="expression string to evaluate")

    parser.add_argument("-m", "--use-modules",
                        metavar="MODULE",
                        type=str,
                        action="store",
                        dest="arg_modules",
                        required=False,
                        default=[],
                        nargs="+",
                        help="additional modules to use")

    args = parser.parse_args()
    return args.expression, args.arg_modules


if __name__ == "__main__":
    print(__doc__)
