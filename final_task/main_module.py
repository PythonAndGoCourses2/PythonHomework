import argparse
import mainclass
import constants
from math import *

argparse.ArgumentParser()

pycalc = mainclass.calculator()

print(pycalc.calculate(str(input())))