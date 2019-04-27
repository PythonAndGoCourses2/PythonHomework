import argparse
import main_funcs
import pycalc_checker
from math import *

argparse.ArgumentParser()

methods = main_funcs.calc_init(['math'])

# sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)

# for item in pycalc_checker.COMMON_TESTS.keys():
# print(main_funcs.calculate(item, methods))
# print(pycalc_checker.COMMON_TESTS[item])

print(main_funcs.calculate('sin(-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0)))))', methods))
print(sin(-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))))

# 'sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))'
