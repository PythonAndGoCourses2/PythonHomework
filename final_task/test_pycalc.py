import unittest
import math
import pycalc


class TestMyCaseCalculator(unittest.TestCase):

    def test_default_arithmetic(self):
        self.assertEqual(pycalc.main('2+2'), 2+2)
        self.assertEqual(pycalc.main('2*2'), 2*2)
        self.assertEqual(pycalc.main('2-2'), 2-2)
        self.assertEqual(pycalc.main('2/2'), 2/2)
        self.assertEqual(pycalc.main('2^2'), 2**2)
        self.assertEqual(pycalc.main('2//2'), 2//2)
        self.assertEqual(pycalc.main('2%2'), 2%2)

    def test_more_than_one_number(self):
        self.assertEqual(pycalc.main('22+22'), 22+22)
        self.assertEqual(pycalc.main('222+222'), 222+222)

    def test_module_math_trigonometry(self):
        self.assertEqual(pycalc.main('sin(90)'), math.sin(90))
        self.assertEqual(pycalc.main('cos(90)'), math.cos(90))
        self.assertEqual(pycalc.main('tan(90)'), math.tan(90))
        self.assertEqual(pycalc.main('asin(1)'), math.asin(1))
        self.assertEqual(pycalc.main('acos(0)'), math.acos(0))
        self.assertEqual(pycalc.main('atan(1)'), math.atan(1))
        self.assertEqual(pycalc.main('hypot(3,4)'), math.hypot(3, 4))
        self.assertEqual(pycalc.main('degrees(3.14)'), math.degrees(3.14))
        self.assertEqual(pycalc.main('radians(90)'), math.radians(90))
        self.assertEqual(pycalc.main('sinh(1)'), math.sinh(1))
        self.assertEqual(pycalc.main('cosh(1)'), math.cosh(1))
        self.assertEqual(pycalc.main('tanh(1)'), math.tanh(1))
        self.assertEqual(pycalc.main('asinh(1)'), math.asinh(1))
        self.assertEqual(pycalc.main('acosh(1)'), math.acosh(1))
        self.assertEqual(pycalc.main('atanh(0)'), math.atanh(0))
        self.assertEqual(pycalc.main('pi'), math.pi)
        self.assertEqual(pycalc.main('e'), math.e)
        self.assertEqual(pycalc.main('tau'), math.tau)

    def test_module_math_arithmetic(self):
        self.assertEqual(pycalc.main('ceil(3.14)'), math.ceil(3.14))
        self.assertEqual(pycalc.main('copysign(-1,-2)'), math.copysign(-1, -2))
        self.assertEqual(pycalc.main('fabs(-13)'), math.fabs(-13))
        self.assertEqual(pycalc.main('factorial(5)'), math.factorial(5))
        self.assertEqual(pycalc.main('floor(3.4)'), math.floor(3.4))
        self.assertEqual(pycalc.main('fmod(5,4)'), math.fmod(5, 4))
        self.assertEqual(pycalc.main('frexp(300000)'), math.frexp(300000))
        self.assertEqual(pycalc.main('ldexp(3,10)'), math.ldexp(3,10))
        self.assertEqual(pycalc.main('fsum([3,4,5])'), math.fsum([3, 4, 5]))
        self.assertEqual(pycalc.main('isfinite(3)'), math.isfinite(3))
        self.assertEqual(pycalc.main('isinf(3)'), math.isinf(3))
        self.assertEqual(pycalc.main('isnan(3)'), math.isnan(3))
        self.assertEqual(pycalc.main('modf(-3)'), math.modf(-3))
        self.assertEqual(pycalc.main('trunc(3.4)'), math.trunc(3.4))
        self.assertEqual(pycalc.main('exp(3)'), math.exp(3))
        self.assertEqual(pycalc.main('expm1(3)'), math.expm1(3))
        self.assertEqual(pycalc.main('log(10,2)'), math.log(10, 2))
        self.assertEqual(pycalc.main('log1p(10)'), math.log1p(10))
        self.assertEqual(pycalc.main('log10(10)'), math.log10(10))
        self.assertEqual(pycalc.main('log2(10)'), math.log2(10))
        self.assertEqual(pycalc.main('pow(2,3)'), math.pow(2, 3))
        self.assertEqual(pycalc.main('sqrt(25)'), math.sqrt(25))
        self.assertEqual(pycalc.main('erf(3)'), math.erf(3))
        self.assertEqual(pycalc.main('erfc(3)'), math.erfc(3))
        self.assertEqual(pycalc.main('gamma(3)'), math.gamma(3))
        self.assertEqual(pycalc.main('lgamma(3)'), math.lgamma(3))

    def test_round_brackets(self):
        self.assertEqual(pycalc.main('(2+2)*2'), (2+2)*2)
        self.assertEqual(pycalc.main('(2+2)*2+(2+2)'), (2+2)*2+(2+2))
        self.assertEqual(pycalc.main('2+(2+(2+3)+3)+2'), 2+(2+(2+3)+3)+2)
        self.assertEqual(pycalc.main('2+(2+3)*3+2'), 2+(2+3)*3+2)
        self.assertEqual(pycalc.main('((2+2)*3)+2'), ((2+2)*3)+2)

    def test_with_floating_numbers(self):
        self.assertEqual(pycalc.main('2.3+2.3'), 2.3+2.3)


class TestEpamCaseCalculator(unittest.TestCase):

    def test_unary_operators(self):
        self.assertEqual(pycalc.main("-13"), -13)
        self.assertEqual(pycalc.main("6-(-13)"), 6-(-13))
        self.assertEqual(pycalc.main("1---1"), 1---1)
        self.assertEqual(pycalc.main("-+---+-1"), -+---+-1)

    def test_operation_priority(self):
        self.assertEqual(pycalc.main("1+2*2"), 1+2*2)
        self.assertEqual(pycalc.main("1+(2+3*2)*3"), 1+(2+3*2)*3)
        self.assertEqual(pycalc.main("10*(2+1)"), 10*(2+1))
        self.assertEqual(pycalc.main("10^(2+1)"), 10**(2+1))
        self.assertEqual(pycalc.main("100/3^2"), 100/3**2)
        self.assertEqual(pycalc.main("100/3%2^2"), 100/3%2**2)

    def test_functions_and_constants(self):
        self.assertEqual(pycalc.main("pi+e"), math.pi+math.e)
        self.assertEqual(pycalc.main("log(e)"), math.log(math.e))
        self.assertEqual(pycalc.main("sin(pi/2)"), math.sin(math.pi/2))
        self.assertEqual(pycalc.main("log10(100)"), math.log10(100))
        self.assertEqual(pycalc.main("sin(pi/2)*111*6"), math.sin(math.pi/2)*111*6)
        self.assertEqual(pycalc.main("2*sin(pi/2)"), 2*math.sin(math.pi/2))

    def test_associative(self):
        self.assertEqual(pycalc.main("102%12%7"), 102%12%7)
        self.assertEqual(pycalc.main("100/4/3"), 100/4/3)
        self.assertEqual(pycalc.main("2^3^4"), 2**3**4)

    def test_comparison_operators(self):
        self.assertEqual(pycalc.main("1+2*3==1+2*3"), 1+2*3==1+2*3)
        self.assertAlmostEqual(pycalc.main("e^5>=e^5+1"), math.e**5>=math.e**5+1)
        self.assertAlmostEqual(pycalc.main("1+2*4/3+1!=1+2*4/3+2"), 1+2*4/3+1!=1+2*4/3+2)

    def test_common_tests(self):
        self.assertEqual(pycalc.main("(100)"), (100))
        self.assertEqual(pycalc.main("666"), 666)
        self.assertEqual(pycalc.main("-.1"), -.1)
        self.assertEqual(pycalc.main("1/3"), 1/3)
        self.assertEqual(pycalc.main("1.0/3.0"), 1.0/3.0)
        self.assertEqual(pycalc.main(".1 * 2.0^56.0"), .1 * 2.0**56.0)
        self.assertEqual(pycalc.main("e^34"), math.e**34)
        self.assertEqual(pycalc.main("(2.0^(pi/pi+e/e+2.0^0.0))"), (2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0)))
        self.assertEqual(pycalc.main("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"), (2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))**(1.0/3.0))
        self.assertEqual(pycalc.main("sin(pi/2^1) + log(1*4+2^2+1, 3^2)"), math.sin(math.pi/2**1) + math.log(1*4+2**2+1, 3**2))
        self.assertEqual(pycalc.main("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"), 10*math.e**0*math.log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5)
        self.assertEqual(pycalc.main("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)"), math.sin(-math.cos(-math.sin(3.0)-math.cos(-math.sin(-3.0*5.0)-math.sin(math.cos(math.log10(43.0))))+math.cos(math.sin(math.sin(34.0-2.0**2.0))))--math.cos(1.0)--math.cos(0.0)**3.0))
        self.assertEqual(pycalc.main("2.0^(2.0^2.0*2.0^2.0)"), 2.0**(2.0**2.0*2.0**2.0))
        self.assertEqual(pycalc.main("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"), math.sin(math.e**math.log(math.e**math.e**math.sin(23.0),45.0) + math.cos(3.0+math.log10(math.e**-math.e))))
