import argparse
from src import calculate


def calc():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "expression", help="Enter expression to evaluate", type=str)
    args = parser.parse_args()
    try:
        print(calculate.calculate(args.expression))
    except Exception as err:
        print("ERROR: {0}".format(err))
