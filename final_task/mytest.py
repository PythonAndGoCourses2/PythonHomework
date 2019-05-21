import unittest
import math
from math import *
import pycalc

# -15//2=-8
# 0-15//2=-7
# 0+15//2=7
# 0- -15//2=8
# 0+-(-15)//2=7

print("-15//2=-8", ">>>>", pycalc.calc("-15//2"))
print("0-15//2=-7", ">>>>", pycalc.calc("0-15//2"))
print("0+15//2=7", ">>>>", pycalc.calc("0+15//2"))
print("0- -15//2=8", ">>>>", pycalc.calc("0- -15//2"))
print("0+-(-15)//2=7", ">>>>", pycalc.calc("0+-(-15)//2"))

print("2+-(3+4)", ">>>>", pycalc.calc("2+-(3+4)"))
print("2--(3+4)", ">>>>", pycalc.calc("2--(3+4)"))
print("2/-sin(3+4)", ">>>>", pycalc.calc("2/-sin(3+4)"))
print("2+-(3)+4", ">>>>", pycalc.calc("2+-(3)+4"))
print("2+-3/2)", ">>>>", pycalc.calc("2+-3/2)"))

print("2+2^3^4", ">>>>", pycalc.brackets4exp("2+2^3^4"))
print("2+2^1-3^4", ">>>>", pycalc.brackets4exp("2+2^1-3^4"))
print("2+2^3^4/2", ">>>>", pycalc.brackets4exp("2+2^3^4/2"))
print("2+2^3^4/2+1", ">>>>", pycalc.brackets4exp("2+2^3^4/2+1"))
print("(2+2)^(3-1)^4+2", ">>>>", pycalc.brackets4exp("(2+2)^(3-1)^4+2"))
