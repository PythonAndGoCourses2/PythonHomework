import argparse
from calculate import calculate


parser = argparse.ArgumentParser()
parser.add_argument("expression", help="Enter expression to evaluate", type=str)
args = parser.parse_args()
try:
    print(calculate(args.expression))
except ValueError as err:
    print("ERROR: "+err)
