import unittest
import pycalc
import math
from math import pi, e, sin, cos, log, log10


class CheckCalculator(unittest.TestCase):

    def test_sum(self):
        # Unary operators:
        self.assertEqual(pycalc.check_entrence("-13"), eval("-13"), "FAILED")
        self.assertEqual(pycalc.check_entrence("6-(-13)"), eval("6-(-13)"), "FAILED")
        # Multiple use of operators:
        self.assertEqual(pycalc.check_entrence("1---1"), eval("1---1"), "FAILED")
        self.assertEqual(pycalc.check_entrence("-+---+-1"), eval("-+---+-1"), "FAILED")

        # Operation priority
        self.assertEqual(pycalc.check_entrence("1+2*2"), eval("1+2*2"), "FAILED")
        self.assertEqual(pycalc.check_entrence("1+(2+3*2)*3"), eval("1+(2+3*2)*3"), "FAILED")
        self.assertEqual(pycalc.check_entrence("10*(2+1)"), eval("10*(2+1)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("10^(2+1)"), eval("10**(2+1)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("100/3^2"), eval("100/3**2"), "FAILED")
        self.assertEqual(pycalc.check_entrence("100/3%2^2"), eval("100/3%2**2"), "FAILED")

        # Functions and constants
        self.assertEqual(pycalc.check_entrence("pi+e"), eval("pi+e"), "FAILED")
        self.assertEqual(pycalc.check_entrence("log(e)"), eval("log(e)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("sin(pi/2)"), eval("sin(pi/2)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("log10(100)"), eval("log10(100)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("sin(pi/2)*111*6"), eval("sin(pi/2)*111*6"), "FAILED")
        self.assertEqual(pycalc.check_entrence("2*sin(pi/2)"), eval("2*sin(pi/2)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("abs(-5)"), eval("abs(-5)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("round(123.456789)"), eval("round(123.456789)"), "FAILED")

        # Associative
        self.assertEqual(pycalc.check_entrence("102%12%7"), eval("102%12%7"), "FAILED")
        self.assertEqual(pycalc.check_entrence("100/4/3"), eval("100/4/3"), "FAILED")
        self.assertEqual(pycalc.check_entrence("2^3^4"), eval("2**3**4"), "FAILED")

        # Comparison operators
        self.assertEqual(pycalc.check_entrence("1+2*3==1+2*3"), eval("1+2*3==1+2*3"), "FAILED")
        self.assertEqual(pycalc.check_entrence("e^5>=e^5+1"), eval("math.e**5>=math.e**5+1"), "FAILED")
        self.assertEqual(pycalc.check_entrence("1+2*4/3+1!=1+2*4/3+2"), eval("1+2*4/3+1!=1+2*4/3+2"), "FAILED")

        # Common tests
        self.assertEqual(pycalc.check_entrence("(100)"), eval("(100)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("666"), eval("666"), "FAILED")
        self.assertEqual(pycalc.check_entrence("-.1"), eval("-.1"), "FAILED")
        self.assertEqual(pycalc.check_entrence("1/3"), eval("1/3"), "FAILED")
        self.assertEqual(pycalc.check_entrence("1.0/3.0"), eval("1.0/3.0"), "FAILED")
        self.assertEqual(pycalc.check_entrence(".1 * 2.0^56.0"), eval(".1 * 2.0**56.0"), "FAILED")
        self.assertEqual(pycalc.check_entrence("e^34"), eval("e**34"), "FAILED")
        self.assertEqual(pycalc.check_entrence("(2.0^(pi/pi+e/e+2.0^0.0))"), eval("(2.0**(pi/pi+e/e+2.0**0.0))"),
                         "FAILED")
        self.assertEqual(pycalc.check_entrence("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"),
                         eval("(2.0**(pi/pi+e/e+2.0**0.0))**(1.0/3.0)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("sin(pi/2^1) + log(1*4+2^2+1, 3^2)"),
                         eval("sin(pi/2**1) + log(1*4+2**2+1, 3**2)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"),
                         eval("10*e**0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"), "FAILED")
        self.assertEqual(pycalc.check_entrence(
            "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos("
            "1.0)--cos(0.0)^3.0)"),
            eval(
                "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0**2.0))))--cos("
                "1.0)--cos(0.0)**3.0)"),
            "FAILED")
        self.assertEqual(pycalc.check_entrence("2.0^(2.0^2.0*2.0^2.0)"), eval("2.0**(2.0**2.0*2.0**2.0)"), "FAILED")
        self.assertEqual(pycalc.check_entrence("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"),
                         eval("sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e)))"), "FAILED")

        # Error cases
        self.assertEqual(pycalc.check_entrence(""), "ERROR:Invalid syntax", "FAILED")
        self.assertEqual(pycalc.check_entrence("+"), "ERROR:Invalid syntax", "FAILED")
        self.assertEqual(pycalc.check_entrence("1-"), "ERROR:Invalid syntax", "FAILED")
        self.assertEqual(pycalc.check_entrence("1 2"), "ERROR: You have no operators or functions between digits.",
                         "FAILED")
        self.assertEqual(pycalc.check_entrence("ee"), "ERROR:Invalid syntax", "FAILED")
        self.assertEqual(pycalc.check_entrence("==7"), "ERROR:Invalid syntax", "FAILED")
        self.assertEqual(pycalc.check_entrence("1 + 2(3 * 4))"), "ERROR: Brackets are not balanced.", "FAILED")
        self.assertEqual(pycalc.check_entrence("((1+2)"), "ERROR: Brackets are not balanced.", "FAILED")
        self.assertEqual(pycalc.check_entrence("1 + 1 2 3 4 5 6 "),
                         "ERROR: You have no operators or functions between digits.", "FAILED")
        self.assertEqual(pycalc.check_entrence("log100(100)"), "ERROR:Invalid syntax", "FAILED")
        self.assertEqual(pycalc.check_entrence("5 > = 6"),
                         "ERROR: You have to delete space(s) between the operator(s).",
                         "FAILED")
        self.assertEqual(pycalc.check_entrence("5 / / 6"),
                         "ERROR: You have to delete space(s) between the operator(s).",
                         "FAILED")
        self.assertEqual(pycalc.check_entrence("6 < = 6"),
                         "ERROR: You have to delete space(s) between the operator(s).",
                         "FAILED")
        self.assertEqual(pycalc.check_entrence("6 * * 6"), "ERROR:Invalid syntax", "FAILED")
        self.assertEqual(pycalc.check_entrence("((((("), "ERROR: Brackets are not balanced.", "FAILED")
        self.assertEqual(pycalc.check_entrence("pow(2, 3, 4)"), "ERROR:Invalid syntax", "FAILED")


if __name__ == '__main__':
    unittest.main()
