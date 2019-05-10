#!/usr/bin/env python3

"""Pure-python command-line calculator."""


import sys
from .argument_parser import parse, ArgumentParserError
from .import_calc_modules import import_modules, ImportCalculatorModulesError
from .expression_parser import calculate, ExpressionParserError, math_consts, math_funcs


def main():
    try:
        expression, modules = parse()
        imported_math_funcs, imported_math_consts = import_modules(modules)

        math_funcs.update(imported_math_funcs)
        math_consts.update(imported_math_consts)

        result = calculate(expression)

    except (ArgumentParserError, ImportCalculatorModulesError, ExpressionParserError) as err:
        sys.stdout.write(f"ERROR: {err}\n")
        sys.exit(2)
    else:
        print(result)


if __name__ == "__main__":
    main()
