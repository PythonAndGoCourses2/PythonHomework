import unittest
import math
import pycalc


class TestMyCaseCalculator(unittest.TestCase):

    def test_default_arithmetic(self):
        self.assertEqual(pycalc.py_calculator('10+10'), 10+10)
        self.assertEqual(pycalc.py_calculator('2*4'), 2*4)
        self.assertEqual(pycalc.py_calculator('5-6'), 5-6)
        self.assertEqual(pycalc.py_calculator('10/10'), 10/10)
        self.assertEqual(pycalc.py_calculator('10^10'), 10**10)
        self.assertEqual(pycalc.py_calculator('21//2'), 21//2)
        self.assertEqual(pycalc.py_calculator('2%2'), 2 % 2)

    def test_with_floating_numbers(self):
        self.assertEqual(pycalc.py_calculator('0.4 + 1.5'), 0.4 + 1.5)
        self.assertEqual(pycalc.py_calculator('.4 + 1.5'), .4 + 1.5)
        self.assertEqual(pycalc.py_calculator('.4^-1.5'), eval('0.4**-1.5'))

    def test_number_theoretic_and_representation_functions(self):
        self.assertEqual(pycalc.py_calculator('ceil(2.5)'), math.ceil(2.5))
        self.assertEqual(pycalc.py_calculator('copysign(1.0, -1.0)'), math.copysign(1.0, -1.0))
        self.assertEqual(pycalc.py_calculator('fabs(-5)'), math.fabs(-5))
        self.assertEqual(pycalc.py_calculator('factorial(2)'), math.factorial(2))
        self.assertEqual(pycalc.py_calculator('floor(5.5)'), math.floor(5.5))
        self.assertEqual(pycalc.py_calculator('fmod(5,5)'), math.fmod(5, 5))
        self.assertEqual(pycalc.py_calculator('frexp(5)'), math.frexp(5))
        self.assertEqual(pycalc.py_calculator('ldexp(3,10)'), math.ldexp(3, 10))
        self.assertEqual(pycalc.py_calculator('fsum([.1, .1, .1])'), math.fsum([.1, .1, .1]))
        self.assertEqual(pycalc.py_calculator('gcd(5, 10)'), math.gcd(5, 10))
        self.assertEqual(pycalc.py_calculator('isclose(1, 2, rel_tol=0.05, abs_tol=0.0)'),
                         math.isclose(1, 2, rel_tol=0.05, abs_tol=0.0))
        self.assertEqual(pycalc.py_calculator('isfinite(3)'), math.isfinite(3))
        self.assertEqual(pycalc.py_calculator('isinf(3)'), math.isinf(3))
        self.assertEqual(pycalc.py_calculator('isnan(3)'), math.isnan(3))
        self.assertEqual(pycalc.py_calculator('modf(-3)'), math.modf(-3))
        self.assertEqual(pycalc.py_calculator('trunc(3.4)'), math.trunc(3.4))
        self.assertEqual(pycalc.py_calculator('exp(3)'), math.exp(3))
        self.assertEqual(pycalc.py_calculator('expm1(3)'), math.expm1(3))
        self.assertEqual(pycalc.py_calculator('log(10,2)'), math.log(10, 2))
        self.assertEqual(pycalc.py_calculator('log1p(10)'), math.log1p(10))
        self.assertEqual(pycalc.py_calculator('log10(10)'), math.log10(10))
        self.assertEqual(pycalc.py_calculator('log2(10)'), math.log2(10))
        self.assertEqual(pycalc.py_calculator('pow(2,3)'), math.pow(2, 3))
        self.assertEqual(pycalc.py_calculator('sqrt(25)'), math.sqrt(25))
        self.assertEqual(pycalc.py_calculator('erf(3)'), math.erf(3))
        self.assertEqual(pycalc.py_calculator('erfc(3)'), math.erfc(3))
        self.assertEqual(pycalc.py_calculator('gamma(3)'), math.gamma(3))
        self.assertEqual(pycalc.py_calculator('lgamma(3)'), math.lgamma(3))

    def test_module_math_trigonometry(self):
        self.assertEqual(pycalc.py_calculator('sin(90)'), math.sin(90))
        self.assertEqual(pycalc.py_calculator('cos(90)'), math.cos(90))
        self.assertEqual(pycalc.py_calculator('tan(90)'), math.tan(90))
        self.assertEqual(pycalc.py_calculator('asin(1)'), math.asin(1))
        self.assertEqual(pycalc.py_calculator('acos(0)'), math.acos(0))
        self.assertEqual(pycalc.py_calculator('atan(1)'), math.atan(1))
        self.assertEqual(pycalc.py_calculator('hypot(3,4)'), math.hypot(3, 4))
        self.assertEqual(pycalc.py_calculator('degrees(3.14)'), math.degrees(3.14))
        self.assertEqual(pycalc.py_calculator('radians(90)'), math.radians(90))
        self.assertEqual(pycalc.py_calculator('sinh(1)'), math.sinh(1))
        self.assertEqual(pycalc.py_calculator('cosh(1)'), math.cosh(1))
        self.assertEqual(pycalc.py_calculator('tanh(1)'), math.tanh(1))
        self.assertEqual(pycalc.py_calculator('asinh(1)'), math.asinh(1))
        self.assertEqual(pycalc.py_calculator('acosh(1)'), math.acosh(1))
        self.assertEqual(pycalc.py_calculator('atanh(0)'), math.atanh(0))
        self.assertEqual(pycalc.py_calculator('pi'), math.pi)
        self.assertEqual(pycalc.py_calculator('e'), math.e)
        self.assertEqual(pycalc.py_calculator('tau'), math.tau)

    def test_round_brackets(self):
        self.assertEqual(pycalc.py_calculator('(2+2)*2'), (2+2)*2)
        self.assertEqual(pycalc.py_calculator('(2+2)*2+(2+2)'), (2+2)*2+(2+2))
        self.assertEqual(pycalc.py_calculator('2+(2+(2+3)+3)+2'), 2+(2+(2+3)+3)+2)
        self.assertEqual(pycalc.py_calculator('2+(2+3)*3+2'), 2+(2+3)*3+2)
        self.assertEqual(pycalc.py_calculator('((2+2)*3)+2'), ((2+2)*3)+2)


class TestEpamCaseCalculator(unittest.TestCase):

    def test_unary_operators(self):
        self.assertEqual(pycalc.py_calculator("-13"), -13)
        self.assertEqual(pycalc.py_calculator("6-(-13)"), 6-(-13))
        self.assertEqual(pycalc.py_calculator("1---1"), 1---1)
        self.assertEqual(pycalc.py_calculator("-+---+-1"), -+---+-1)

    def test_operation_priority(self):
        self.assertEqual(pycalc.py_calculator("1+2*2"), 1+2*2)
        self.assertEqual(pycalc.py_calculator("1+(2+3*2)*3"), 1+(2+3*2)*3)
        self.assertEqual(pycalc.py_calculator("10*(2+1)"), 10*(2+1))
        self.assertEqual(pycalc.py_calculator("10^(2+1)"), 10**(2+1))
        self.assertEqual(pycalc.py_calculator("100/3^2"), 100/3**2)
        self.assertEqual(pycalc.py_calculator("100/3%2^2"), 100/3 % 2**2)

    def test_functions_and_constants(self):
        self.assertEqual(pycalc.py_calculator("pi+e"), math.pi+math.e)
        self.assertEqual(pycalc.py_calculator("log(e)"), math.log(math.e))
        self.assertEqual(pycalc.py_calculator("sin(pi/2)"), math.sin(math.pi/2))
        self.assertEqual(pycalc.py_calculator("log10(100)"), math.log10(100))
        self.assertEqual(pycalc.py_calculator("sin(pi/2)*111*6"), math.sin(math.pi/2)*111*6)
        self.assertEqual(pycalc.py_calculator("2*sin(pi/2)"), 2*math.sin(math.pi/2))
        self.assertEqual(pycalc.py_calculator("pow(2, 3)"), math.pow(2, 3))
        self.assertEqual(pycalc.py_calculator("abs(-5)"), abs(-5))
        self.assertEqual(pycalc.py_calculator("round(123.4567890)"), round(123.4567890))

    def test_associative(self):
        self.assertEqual(pycalc.py_calculator("102%12%7"), 102 % 12 % 7)
        self.assertEqual(pycalc.py_calculator("100/4/3"), 100/4/3)
        self.assertEqual(pycalc.py_calculator("2^3^4"), 2**3**4)

    def test_comparison_operators(self):
        self.assertEqual(pycalc.py_calculator("1+2*3==1+2*3"), 1+2*3 == 1+2*3)
        self.assertAlmostEqual(pycalc.py_calculator("e^5>=e^5+1"), math.e**5 >= math.e**5+1)
        self.assertAlmostEqual(pycalc.py_calculator("1+2*4/3+1!=1+2*4/3+2"), 1+2*4/3+1 != 1+2*4/3+2)

    def test_common_tests(self):
        self.assertEqual(pycalc.py_calculator("(100)"), eval("(100)"))
        self.assertEqual(pycalc.py_calculator("666"), 666)
        self.assertEqual(pycalc.py_calculator("-.1"), -.1)
        self.assertEqual(pycalc.py_calculator("1/3"), 1/3)
        self.assertEqual(pycalc.py_calculator("1.0/3.0"), 1.0/3.0)
        self.assertEqual(pycalc.py_calculator(".1 * 2.0^56.0"), .1 * 2.0**56.0)
        self.assertEqual(pycalc.py_calculator("e^34"), math.e**34)
        self.assertEqual(pycalc.py_calculator("(2.0^(pi/pi+e/e+2.0^0.0))"),
                         (2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0)))
        self.assertEqual(pycalc.py_calculator("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"),
                         (2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))**(1.0/3.0))
        self.assertEqual(pycalc.py_calculator("sin(pi/2^1) + log(1*4+2^2+1, 3^2)"),
                         math.sin(math.pi/2**1) + math.log(1*4+2**2+1, 3**2))
        self.assertEqual(pycalc.py_calculator("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"),
                         10*math.e**0*math.log10(.4 - 5 / -0.1-10) - -abs(-53/10) + -5)
        expression = "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+" \
                     "cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)"
        self.assertEqual(pycalc.py_calculator(expression),
                         math.sin(-math.cos(-math.sin(3.0)-math.cos(-math.sin(-3.0*5.0) -
                                                                    math.sin(math.cos(math.log10(43.0))))
                                            + math.cos(math.sin(math.sin(34.0-2.0**2.0))))--math.cos(1.0) -
                                  -math.cos(0.0)**3.0))
        self.assertEqual(pycalc.py_calculator("2.0^(2.0^2.0*2.0^2.0)"), 2.0**(2.0**2.0*2.0**2.0))
        self.assertEqual(pycalc.py_calculator("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"),
                         math.sin(math.e**math.log(math.e**math.e**math.sin(23.0), 45.0) +
                         math.cos(3.0+math.log10(math.e**-math.e))))

    def test_Error_cases(self):
        self.assertRaises(ValueError, pycalc.py_calculator, "")
        self.assertRaises(ValueError, pycalc.py_calculator, "+")
        self.assertRaises(ValueError, pycalc.py_calculator, "1-")
        self.assertRaises(ValueError, pycalc.py_calculator, "1 2")
        self.assertRaises(ValueError, pycalc.py_calculator, "==7")
        self.assertRaises(ValueError, pycalc.py_calculator, "1 + 2(3 * 4))")
        self.assertRaises(ValueError, pycalc.py_calculator, "((1+2)")
        self.assertRaises(ValueError, pycalc.py_calculator, "1 + 1 2 3 4 5 6 ")
        self.assertRaises(ValueError, pycalc.py_calculator, "log100(100)")
        self.assertRaises(ValueError, pycalc.py_calculator, "------")
        self.assertRaises(ValueError, pycalc.py_calculator, "5 > = 6")
        self.assertRaises(ValueError, pycalc.py_calculator, "5 / / 6")
        self.assertRaises(ValueError, pycalc.py_calculator, "6 < = 6")
        self.assertRaises(ValueError, pycalc.py_calculator, "6 * * 6")
        self.assertRaises(ValueError, pycalc.py_calculator, "(((((")
        self.assertRaises(ValueError, pycalc.py_calculator, "abs")
        self.assertRaises(ValueError, pycalc.py_calculator, "pow(2, 3, 4)")


if __name__ == '__main__':
    unittest.main()
