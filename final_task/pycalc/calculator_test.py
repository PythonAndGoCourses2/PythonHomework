import unittest
from . import calculator
import math


class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calculator = calculator.Calculator()

    def testUnary(self):
        iExpr = "-13"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = "6-(-13)"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = "1---1"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = "-+---+-1"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))

    def testOppriority(self):
        iExpr = "1+2*2"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = "1+(2+3*2)*3"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = "10*(2+1)"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = "10^(2+1)"
        self.assertEqual(self.calculator.calculate(iExpr), eval("10**(2+1)"))
        iExpr = "100/3^2"
        self.assertEqual(self.calculator.calculate(iExpr), eval("100/3**2"))
        iExpr = "100/3%2^2"
        self.assertEqual(self.calculator.calculate(iExpr), eval("100/3%2**2"))

    def testFunc(self):
        iExpr = "pi+e"
        self.assertEqual(self.calculator.calculate(iExpr), eval("math.pi+math.e"))
        iExpr = "log(e)"
        self.assertEqual(self.calculator.calculate(iExpr), eval("math.log(math.e)"))
        iExpr = "sin(pi/2)"
        self.assertEqual(self.calculator.calculate(iExpr), eval("math.sin(math.pi/2)"))
        iExpr = "log10(100)"
        self.assertEqual(self.calculator.calculate(iExpr), eval("math.log10(100)"))
        iExpr = "sin(pi/2)*111*6"
        self.assertEqual(
            self.calculator.calculate(iExpr), eval("math.sin(math.pi/2)*111*6")
        )
        iExpr = "2*sin(pi/2)"
        self.assertEqual(
            self.calculator.calculate(iExpr), eval("2*math.sin(math.pi/2)")
        )
        iExpr = "2^3^2^2"
        self.assertEqual(self.calculator.calculate(iExpr), eval("2**3**2**2"))

    def testAssociative(self):
        iExpr = r"102%12%7"
        self.assertEqual(self.calculator.calculate(iExpr), eval(r"102%12%7"))
        iExpr = "100/4/3"
        self.assertEqual(self.calculator.calculate(iExpr), eval("100/4/3"))
        iExpr = "2^3^4"
        self.assertEqual(self.calculator.calculate(iExpr), eval("2**3**4"))

    def testComparison(self):
        iExpr = r"1+2*3==1+2*3"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = r"e^5>=e^5+1"
        self.assertEqual(
            self.calculator.calculate(iExpr), eval("math.e**5>=math.e**5+1")
        )
        iExpr = r"1+2*4/3+1!=1+2*4/3+2"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))

    def testCommon(self):
        iExpr = r"(100)"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = r"666"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = r"-.1"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = r"1/3"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = r"1.0/3.0"
        self.assertEqual(self.calculator.calculate(iExpr), eval(iExpr))
        iExpr = r".1 * 2.0^56.0"
        self.assertEqual(self.calculator.calculate(iExpr), eval(".1 * 2.0**56.0"))
        iExpr = r"e^34"
        self.assertEqual(self.calculator.calculate(iExpr), eval("math.e**34"))
        iExpr = r"(2.0^(pi/pi+e/e+2.0^0.0))"
        self.assertEqual(
            self.calculator.calculate(iExpr),
            eval("(2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))"),
        )
        iExpr = r"(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"
        self.assertEqual(
            self.calculator.calculate(iExpr),
            eval("(2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))**(1.0/3.0)"),
        )
        iExpr = r"sin(pi/2^1) + log(1*4+2^2+1, 3^2)"
        self.assertEqual(
            self.calculator.calculate(iExpr),
            eval("math.sin(math.pi/2**1) + math.log(1*4+2**2+1, 3**2)"),
        )
        iExpr = r"10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"
        self.assertEqual(
            self.calculator.calculate(iExpr),
            eval("10*math.e**0*math.log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"),
        )

        iExpr = r"2.0^(2.0^2.0*2.0^2.0)"
        self.assertEqual(
            self.calculator.calculate(iExpr), eval("2.0**(2.0**2.0*2.0**2.0)")
        )
        iExpr = r"sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"
        self.assertEqual(
            self.calculator.calculate(iExpr),
            eval(
                "math.sin(math.e**math.log(math.e**math.e**math.sin(23.0),45.0) + math.cos(3.0+math.log10(math.e**-math.e)))"
            ),
        )

    """def testError(self):
        iExpr = r"((1+2)"
        with self.assertRaises(converter.ConvertError):
            self.calculator.calculate(iExpr)
        iExpr = r""
        with self.assertRaises(ValueError):
            self.calculator.calculate(iExpr)

        iExpr = r"((((("
        with self.assertRaises(converter.ConvertError):
            self.calculator.calculate(iExpr)
        iExpr = r"1 + 1 2 3 4 5 6"
        with self.assertRaises(ValueError):
            self.calculator.calculate(iExpr)
        iExpr = r"1 2"
        with self.assertRaises(ValueError):
            self.calculator.calculate(iExpr)
        iExpr = r"5 > = 6"
        with self.assertRaises(ValueError):
            self.calculator.calculate(iExpr)
        iExpr = r"5 / / 6"
        with self.assertRaises(ValueError):
            self.calculator.calculate(iExpr)
        iExpr = r"6 < = 6"
        with self.assertRaises(ValueError):
            self.calculator.calculate(iExpr)
        iExpr = r"6 * * 6"
        with self.assertRaises(ValueError):
            self.calculator.calculate(iExpr)
        iExpr = r"log100(100)"
        with self.assertRaises(ValueError):
            self.calculator.calculate(iExpr)
"""


if __name__ == "__main__":

    unittest.main()
