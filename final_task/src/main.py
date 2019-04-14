import argparse
import expParser


parser = argparse.ArgumentParser()
#parser.add_argument("expression", help="Enter expression to evaluate", type=str)
args = parser.parse_args()
#expression = args.expression
expParser.parseToPPN("12*log(abs(45-80))")
try:
    print(expParser.calculate())
except Exception as err:
    print(err)