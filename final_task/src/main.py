import argparse
from src import calculate
def calc():
    parser = argparse.ArgumentParser()
    parser.add_argument("expression", help="Enter expression to evaluate", type=str)
    args = parser.parse_args()
    try:
        print(calculate.calculate(args.expression))
    except ValueError as err:
        print("ERROR: "+ err.str())
