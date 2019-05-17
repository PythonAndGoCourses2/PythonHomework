import unittest
import math
import pycalc


class TestMyCaseCalculator(unittest.TestCase):

    def test_default_arithmetic(self):
        self.assertEqual(pycalc.calc('10+10'), 10+10)
        self.assertEqual(pycalc.calc('2*4'), 2*4)
        self.assertEqual(pycalc.calc('5-6'), 5-6)
        self.assertEqual(pycalc.calc('10/10'), 10/10)
        self.assertEqual(pycalc.calc('10^10'), 10**10)
        self.assertEqual(pycalc.calc('21//2'), 21//2)
        self.assertEqual(pycalc.calc('2%2'), 2 % 2)

    def test_with_floating_numbers(self):
        self.assertEqual(pycalc.calc('0.4 + 1.5'), 0.4 + 1.5)
        self.assertEqual(pycalc.calc('.4 + 1.5'), .4 + 1.5)
        self.assertEqual(pycalc.calc('.4^-(1.5+0.5)'), eval('.4**-(1.5+0.5)'))

    def test_number_theoretic_and_representation_functions(self):
        self.assertEqual(pycalc.calc('ceil(2.5)'), math.ceil(2.5))
        self.assertEqual(pycalc.calc('copysign(1.0, -1.0)'), math.copysign(1.0, -1.0))
        self.assertEqual(pycalc.calc('fabs(-5)'), math.fabs(-5))
        self.assertEqual(pycalc.calc('factorial(2)'), math.factorial(2))
        self.assertEqual(pycalc.calc('floor(5.5)'), math.floor(5.5))
        self.assertEqual(pycalc.calc('fmod(5,5)'), math.fmod(5, 5))
        self.assertEqual(pycalc.calc('frexp(5)'), math.frexp(5))
        self.assertEqual(pycalc.calc('ldexp(3,10)'), math.ldexp(3, 10))
        self.assertEqual(pycalc.calc('fsum([.1, .1, .1])'), math.fsum([.1, .1, .1]))
        self.assertEqual(pycalc.calc('fsum({1:2, 5:8, 6:120})'), math.fsum({1: 2, 5: 8, 6: 120}))
        self.assertEqual(pycalc.calc('gcd(5, 10)'), math.gcd(5, 10))
        self.assertEqual(pycalc.calc('isclose(1, 2, rel_tol=0.05, abs_tol=0.0)'),
                         math.isclose(1, 2, rel_tol=0.05, abs_tol=0.0))
        self.assertEqual(pycalc.calc('isclose(1, 2)'),
                         math.isclose(1, 2))
        self.assertEqual(pycalc.calc('isclose(1, 2, rel_tol=0.05)'),
                         math.isclose(1, 2, rel_tol=0.05))
        self.assertEqual(pycalc.calc('isfinite(3)'), math.isfinite(3))
        self.assertEqual(pycalc.calc('isinf(3)'), math.isinf(3))
        self.assertEqual(pycalc.calc('isnan(3)'), math.isnan(3))
        self.assertEqual(pycalc.calc('modf(-3)'), math.modf(-3))
        self.assertEqual(pycalc.calc('trunc(3.4)'), math.trunc(3.4))
        self.assertEqual(pycalc.calc('exp(3)'), math.exp(3))
        self.assertEqual(pycalc.calc('expm1(3)'), math.expm1(3))
        self.assertEqual(pycalc.calc('log(10,2)'), math.log(10, 2))
        self.assertEqual(pycalc.calc('log1p(10)'), math.log1p(10))
        self.assertEqual(pycalc.calc('log10(10)'), math.log10(10))
        self.assertEqual(pycalc.calc('log2(10)'), math.log2(10))
        self.assertEqual(pycalc.calc('pow(2,3)'), math.pow(2, 3))
        self.assertEqual(pycalc.calc('sqrt(25)'), math.sqrt(25))
        self.assertEqual(pycalc.calc('erf(3)'), math.erf(3))
        self.assertEqual(pycalc.calc('erfc(3)'), math.erfc(3))
        self.assertEqual(pycalc.calc('gamma(3)'), math.gamma(3))
        self.assertEqual(pycalc.calc('lgamma(3)'), math.lgamma(3))

    def test_module_math_trigonometry(self):
        self.assertEqual(pycalc.calc('sin(90)'), math.sin(90))
        self.assertEqual(pycalc.calc('cos(90)'), math.cos(90))
        self.assertEqual(pycalc.calc('tan(90)'), math.tan(90))
        self.assertEqual(pycalc.calc('asin(1)'), math.asin(1))
        self.assertEqual(pycalc.calc('acos(0)'), math.acos(0))
        self.assertEqual(pycalc.calc('atan(1)'), math.atan(1))
        self.assertEqual(pycalc.calc('hypot(3,4)'), math.hypot(3, 4))
        self.assertEqual(pycalc.calc('degrees(3.14)'), math.degrees(3.14))
        self.assertEqual(pycalc.calc('radians(90)'), math.radians(90))
        self.assertEqual(pycalc.calc('sinh(1)'), math.sinh(1))
        self.assertEqual(pycalc.calc('cosh(1)'), math.cosh(1))
        self.assertEqual(pycalc.calc('tanh(1)'), math.tanh(1))
        self.assertEqual(pycalc.calc('asinh(1)'), math.asinh(1))
        self.assertEqual(pycalc.calc('acosh(1)'), math.acosh(1))
        self.assertEqual(pycalc.calc('atanh(0)'), math.atanh(0))
        self.assertEqual(pycalc.calc('pi'), math.pi)
        self.assertEqual(pycalc.calc('e'), math.e)
        self.assertEqual(pycalc.calc('tau'), math.tau)

    def test_round_brackets(self):
        self.assertEqual(pycalc.calc('(2+2)*2'), (2+2)*2)
        self.assertEqual(pycalc.calc('(2+2)*2+(2+2)'), (2+2)*2+(2+2))
        self.assertEqual(pycalc.calc('2+(2+(2+3)+3)+2'), 2+(2+(2+3)+3)+2)
        self.assertEqual(pycalc.calc('2+(2+3)*3+2'), 2+(2+3)*3+2)
        self.assertEqual(pycalc.calc('((2+2)*3)+2'), ((2+2)*3)+2)


class TestEpamCaseCalculator(unittest.TestCase):

    def test_unary_operators(self):
        self.assertEqual(pycalc.calc("-13"), -13)
        self.assertEqual(pycalc.calc("6-(-13)"), 6-(-13))
        self.assertEqual(pycalc.calc("1---1"), 1---1)
        self.assertEqual(pycalc.calc("-+---+-1"), -+---+-1)

    def test_operation_priority(self):
        self.assertEqual(pycalc.calc("1+2*2"), 1+2*2)
        self.assertEqual(pycalc.calc("1+(2+3*2)*3"), 1+(2+3*2)*3)
        self.assertEqual(pycalc.calc("10*(2+1)"), 10*(2+1))
        self.assertEqual(pycalc.calc("10^(2+1)"), 10**(2+1))
        self.assertEqual(pycalc.calc("100/3^2"), 100/3**2)
        self.assertEqual(pycalc.calc("100/3%2^2"), 100/3 % 2**2)

    def test_functions_and_constants(self):
        self.assertEqual(pycalc.calc("pi+e"), math.pi+math.e)
        self.assertEqual(pycalc.calc("log(e)"), math.log(math.e))
        self.assertEqual(pycalc.calc("sin(pi/2)"), math.sin(math.pi/2))
        self.assertEqual(pycalc.calc("log10(100)"), math.log10(100))
        self.assertEqual(pycalc.calc("sin(pi/2)*111*6"), math.sin(math.pi/2)*111*6)
        self.assertEqual(pycalc.calc("2*sin(pi/2)"), 2*math.sin(math.pi/2))
        self.assertEqual(pycalc.calc("pow(2, 3)"), math.pow(2, 3))
        self.assertEqual(pycalc.calc("abs(-5)"), abs(-5))
        self.assertEqual(pycalc.calc("round(123.4567890)"), round(123.4567890))
        self.assertEqual(pycalc.calc("round(123.4567890,2)"), round(123.4567890, 2))

    def test_associative(self):
        self.assertEqual(pycalc.calc("102%12%7"), 102 % 12 % 7)
        self.assertEqual(pycalc.calc("100/4/3"), 100/4/3)
        self.assertEqual(pycalc.calc("2^3^4"), 2**3**4)

    def test_comparison_operators(self):
        self.assertEqual(pycalc.calc("1+2*3==1+2*3"), 1+2*3 == 1+2*3)
        self.assertAlmostEqual(pycalc.calc("e^5>=e^5+1"), math.e**5 >= math.e**5+1)
        self.assertAlmostEqual(pycalc.calc("1+2*4/3+1!=1+2*4/3+2"), 1+2*4/3+1 != 1+2*4/3+2)
        self.assertAlmostEqual(pycalc.calc("True+1"), True + 1)

    def test_common_tests(self):
        self.assertEqual(pycalc.calc("(100)"), eval("(100)"))
        self.assertEqual(pycalc.calc("666"), 666)
        self.assertEqual(pycalc.calc("-.1"), -.1)
        self.assertEqual(pycalc.calc("1/3"), 1/3)
        self.assertEqual(pycalc.calc("1.0/3.0"), 1.0/3.0)
        self.assertEqual(pycalc.calc(".1 * 2.0^56.0"), .1 * 2.0**56.0)
        self.assertEqual(pycalc.calc("e^34"), math.e**34)
        self.assertEqual(pycalc.calc("(2.0^(pi/pi+e/e+2.0^0.0))"),
                         (2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0)))
        self.assertEqual(pycalc.calc("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"),
                         (2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))**(1.0/3.0))
        self.assertEqual(pycalc.calc("sin(pi/2^1) + log(1*4+2^2+1, 3^2)"),
                         math.sin(math.pi/2**1) + math.log(1*4+2**2+1, 3**2))
        self.assertEqual(pycalc.calc("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"),
                         10*math.e**0*math.log10(.4 - 5 / -0.1-10) - -abs(-53/10) + -5)
        expression = "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+" \
                     "cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)"
        self.assertEqual(pycalc.calc(expression),
                         math.sin(-math.cos(-math.sin(3.0)-math.cos(-math.sin(-3.0*5.0) -
                                                                    math.sin(math.cos(math.log10(43.0))))
                                            + math.cos(math.sin(math.sin(34.0-2.0**2.0))))--math.cos(1.0) -
                                  -math.cos(0.0)**3.0))
        self.assertEqual(pycalc.calc("2.0^(2.0^2.0*2.0^2.0)"), 2.0**(2.0**2.0*2.0**2.0))
        self.assertEqual(pycalc.calc("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"),
                         math.sin(math.e**math.log(math.e**math.e**math.sin(23.0), 45.0) +
                         math.cos(3.0+math.log10(math.e**-math.e))))

    def test_Error_cases(self):
        self.assertRaises(ValueError, pycalc.calc, "")
        self.assertRaises(ValueError, pycalc.calc, "+")
        self.assertRaises(ValueError, pycalc.calc, "1-")
        self.assertRaises(ValueError, pycalc.calc, "1 2")
        self.assertRaises(ValueError, pycalc.calc, "==7")
        self.assertRaises(ValueError, pycalc.calc, "1 + 2(3 * 4))")
        self.assertRaises(ValueError, pycalc.calc, "((1+2)")
        self.assertRaises(ValueError, pycalc.calc, "1 + 1 2 3 4 5 6 ")
        self.assertRaises(ValueError, pycalc.calc, "log100(100)")
        self.assertRaises(ValueError, pycalc.calc, "------")
        self.assertRaises(ValueError, pycalc.calc, "5 > = 6")
        self.assertRaises(ValueError, pycalc.calc, "5 / / 6")
        self.assertRaises(ValueError, pycalc.calc, "6 < = 6")
        self.assertRaises(ValueError, pycalc.calc, "6 * * 6")
        self.assertRaises(ValueError, pycalc.calc, "(((((")
        self.assertRaises(ValueError, pycalc.calc, "abs")
        self.assertRaises(ValueError, pycalc.calc, "abs+1")
        self.assertRaises(ValueError, pycalc.calc, "isclose(1)")
        self.assertRaises(ValueError, pycalc.calc, "cos(2,1)")
        self.assertRaises(ValueError, pycalc.calc, "2**2")
        self.assertRaises(ValueError, pycalc.calc, "pow(2, 3, 4)")
        self.assertRaises(ValueError, pycalc.calc, "fsum[1,,2,3]")


if __name__ == '__main__':
    unittest.main()
