import argparse
import sys
from importlib import util
from src import calculate


def calc():
    """run pycalc util"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "expression", help="Enter expression to evaluate", type=str)
    parser.add_argument(
        "-m",
        "--module",
        help="Used to provide external-defined functions. Write full or relative path to your module.",
        type=str)
    args = parser.parse_args()
    try:
        if args.module:
            spec = util.spec_from_file_location("external_module", args.module)
            if not spec:
                raise Exception("Can't find your module")
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(calculate.calculate(args.expression, module))
        else:
            print(calculate.calculate(args.expression))
    except Exception as err:
        print("ERROR: {0}".format(err))
