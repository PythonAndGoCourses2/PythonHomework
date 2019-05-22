import unittest
import math
from math import *
import pycalc


print("2+2^3^4", ">>>>", pycalc.brackets4exp("2+2^3^4"))
print("2+2^1-3^4", ">>>>", pycalc.brackets4exp("2+2^1-3^4"))
print("2+2^3^4/2", ">>>>", pycalc.brackets4exp("2+2^3^4/2"))
print("2+2^3^4/2+1", ">>>>", pycalc.brackets4exp("2+2^3^4/2+1"))
print("(2+2)^(3-1)^4+2", ">>>>", pycalc.brackets4exp("(2+2)^(3-1)^4+2"))


class TestParse(unittest.TestCase):

    def testcases(self):
        self.assertEqual(pycalc.brackets4exp("2^3^4"), "2^(3^4)")
        self.assertEqual(pycalc.brackets4exp("2^3^(4+1)"), "2^(3^(4+1))")
        self.assertEqual(pycalc.brackets4exp("(2+2)^(3-1)^4"), "(2+2)^((3-1)^4)")
        self.assertEqual(pycalc.brackets4exp("(2+2)^(3-1)^4+2"), "(2+2)^((3-1)^4)+2")


class TestPycalc(unittest.TestCase):

    def testcases(self):
        self.assertEqual(pycalc.calc("-13"), eval("-13"))
        self.assertEqual(pycalc.calc("6-(-13)"), eval("6-(-13)"))
        self.assertEqual(pycalc.calc("1---1"), eval("1---1"))
        self.assertEqual(pycalc.calc("-+---+-1"), eval("-+---+-1"))

        self.assertEqual(pycalc.calc("1+2*2"), eval("1+2*2"))
        self.assertEqual(pycalc.calc("1+(2+3*2)*3"), eval("1+(2+3*2)*3"))
        self.assertEqual(pycalc.calc("10*(2+1)"), eval("10*(2+1)"))
        self.assertEqual(pycalc.calc("10^(2+1)"), eval("10**(2+1)"))
        self.assertEqual(pycalc.calc("100/3^2"), eval("100/3**2"))
        self.assertEqual(pycalc.calc("100/3%2^2"), eval("100/3%2**2"))

        self.assertEqual(pycalc.calc("pi+e"), eval("pi+e"))
        self.assertEqual(pycalc.calc("log(e)"), eval("log(e)"))
        self.assertEqual(pycalc.calc("sin(pi/2)"), eval("sin(pi/2)"))
        self.assertEqual(pycalc.calc("log10(100)"), eval("log10(100)"))
        self.assertEqual(pycalc.calc("sin(pi/2)*111*6"), eval("sin(pi/2)*111*6"))
        self.assertEqual(pycalc.calc("2*sin(pi/2)"), eval("2*sin(pi/2)"))
        self.assertEqual(pycalc.calc("abs(-5)"), eval("abs(-5)"))
        self.assertEqual(pycalc.calc("round(123.456789)"), eval("round(123.456789)"))

        self.assertEqual(pycalc.calc("102%12%7"), eval("102%12%7"))
        self.assertEqual(pycalc.calc("100/4/3"), eval("100/4/3"))
        self.assertEqual(pycalc.calc("2^3^4"), eval("2**3**4"))

        self.assertEqual(pycalc.calc("1+2*3==1+2*3"), eval("1+2*3==1+2*3"))
        self.assertEqual(pycalc.calc("e^5>=e^5+1"), eval("e**5>=e**5+1"))
        self.assertEqual(pycalc.calc("1+2*4/3+1!=1+2*4/3+2"), eval("1+2*4/3+1!=1+2*4/3+2"))

        self.assertEqual(pycalc.calc("(100)"), eval("(100)"))
        self.assertEqual(pycalc.calc("666"), eval("666"))
        self.assertEqual(pycalc.calc("-.1"), eval("-.1"))
        self.assertEqual(pycalc.calc("1/3"), eval("1/3"))
        self.assertEqual(pycalc.calc("1.0/3.0"), eval("1.0/3.0"))
        self.assertEqual(pycalc.calc(".1 * 2.0^56.0"), eval(".1 * 2.0**56.0"))
        self.assertEqual(pycalc.calc("e^34"), eval("e**34"))
        self.assertEqual(pycalc.calc("(2.0^(pi/pi+e/e+2.0^0.0))"), eval("(2.0**(pi/pi+e/e+2.0**0.0))"))
        self.assertEqual(pycalc.calc("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"),
                         eval("(2.0**(pi/pi+e/e+2.0**0.0))**(1.0/3.0)"))
        self.assertEqual(pycalc.calc("sin(pi/2^1) + log(1*4+2^2+1, 3^2)"),
                         eval("sin(pi/2**1) + log(1*4+2**2+1, 3**2)"))
        self.assertEqual(pycalc.calc("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"),
                         eval("10*e**0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"))
        self.assertEqual(pycalc.calc("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))"
                         "+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)"),
                         eval("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))"
                         "+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0)"))
        self.assertEqual(pycalc.calc("2.0^(2.0^2.0*2.0^2.0)"), eval("2.0**(2.0**2.0*2.0**2.0)"))
        self.assertEqual(pycalc.calc("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"),
                         eval("sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e)))"))

    def testerrorscases(self):
        self.assertRaises(ValueError, pycalc.calc, "+")
        self.assertRaises(TypeError, pycalc.calc, "1-")
        self.assertRaises(ValueError, pycalc.calc, "1 2")
        self.assertRaises(ValueError, pycalc.calc, "ee")
        self.assertRaises(TypeError, pycalc.calc, "==7")
        self.assertRaises(ValueError, pycalc.calc, "1 + 2(3 * 4))")
        self.assertRaises(ValueError, pycalc.calc, "((1+2)")
        self.assertRaises(ValueError, pycalc.calc, "1 + 1 2 3 4 5 6 ")
        self.assertRaises(ValueError, pycalc.calc, "log100(100)")
        self.assertRaises(ValueError, pycalc.calc, "------")
        self.assertRaises(ValueError, pycalc.calc, "5 > = 6")
        self.assertRaises(ValueError, pycalc.calc, "5 / / 6")
        self.assertRaises(TypeError, pycalc.calc, "6 * * 6")
        self.assertRaises(ValueError, pycalc.calc, "(((((")
        self.assertRaises(ValueError, pycalc.calc, "pow(2, 3, 4)")
