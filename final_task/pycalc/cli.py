"""
Initialize a calculator and calculate
an expression from a command line argument.
"""

import sys

from pycalc.args import args
from pycalc.calculator import calculator
from pycalc.calculator.formatters import err_msg_formatter
from pycalc.calculator.messages import (
    CALCULATOR_INITIALIZATION_ERROR,
    MODULES_IMPORT_ERROR
)
from pycalc.importer.errors import ModuleImportErrors


def main():
    """
    Initialize a calculator and calculate
    an expression from a command line argument.
    """

    # initialize a calculator
    try:
        calc = calculator(args.modules)

    except ModuleImportErrors as exc:
        modules_names = ', '.join(exc.modules_names)
        err_msg = f'{MODULES_IMPORT_ERROR} {modules_names}'
        sys.exit(err_msg_formatter(err_msg))

    except Exception:
        sys.exit(err_msg_formatter(CALCULATOR_INITIALIZATION_ERROR))

    # make a calculation and print a result
    result = calc.calculate(args.expression)
    print(result)


if __name__ == "__main__":
    main()
