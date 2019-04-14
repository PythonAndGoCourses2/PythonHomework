import argparse
import mainclass
import constants
from math import *

argparse.ArgumentParser()

pycalc = mainclass.calculator(constants.imports)

print(pycalc.calculate(str(input())))
print(------6)