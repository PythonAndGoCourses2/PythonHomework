import argparse
from expression import Expression


parser = argparse.ArgumentParser()
#parser.add_argument("expression", help="Enter expression to evaluate", type=str)
args = parser.parse_args()
#expression = args.expression

expression = Expression('12-20*2^2/5*abs(10)')
print(expression.calculate())
