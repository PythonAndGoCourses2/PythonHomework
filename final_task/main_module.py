import argparse
import mainclass
import constants
from math import *

argparse.ArgumentParser()

pycalc = mainclass.calculator()

print(pycalc.calculate(str(input())))
print(sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0**2.0))))))