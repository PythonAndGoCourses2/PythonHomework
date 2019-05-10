import unittest
import math as m
import pycalc


class TestMyCaseCalculator(unittest.TestCase):

    def test_default_arithmetic(self):
        self.assertEqual(pycalc.main('2+2'), 2+2)
        self.assertEqual(pycalc.main('2*2'), 2*2)
        self.assertEqual(pycalc.main('2-2'), 2-2)
        self.assertEqual(pycalc.main('2/2'), 2/2)
        self.assertEqual(pycalc.main('2^2'), 2**2)
        self.assertEqual(pycalc.main('2//2'), 2//2)
        self.assertEqual(pycalc.main('2%2'), 2 % 2)

    def test_more_than_one_number(self):
        self.assertEqual(pycalc.main('22+22'), 22+22)
        self.assertEqual(pycalc.main('222+222'), 222+222)

    def test_module_math_trigonometry(self):
        self.assertEqual(pycalc.main('sin(90)'), m.sin(90))
        self.assertEqual(pycalc.main('cos(90)'), m.cos(90))
        self.assertEqual(pycalc.main('tan(90)'), m.tan(90))
        self.assertEqual(pycalc.main('asin(1)'), m.asin(1))
        self.assertEqual(pycalc.main('acos(0)'), m.acos(0))
        self.assertEqual(pycalc.main('atan(1)'), m.atan(1))
        self.assertEqual(pycalc.main('hypot(3,4)'), m.hypot(3, 4))
        self.assertEqual(pycalc.main('degrees(3.14)'), m.degrees(3.14))
        self.assertEqual(pycalc.main('radians(90)'), m.radians(90))
        self.assertEqual(pycalc.main('sinh(1)'), m.sinh(1))
        self.assertEqual(pycalc.main('cosh(1)'), m.cosh(1))
        self.assertEqual(pycalc.main('tanh(1)'), m.tanh(1))
        self.assertEqual(pycalc.main('asinh(1)'), m.asinh(1))
        self.assertEqual(pycalc.main('acosh(1)'), m.acosh(1))
        self.assertEqual(pycalc.main('atanh(0)'), m.atanh(0))
        self.assertEqual(pycalc.main('pi'), m.pi)
        self.assertEqual(pycalc.main('e'), m.e)
        self.assertEqual(pycalc.main('tau'), m.tau)

    def test_module_math_arithmetic(self):
        self.assertEqual(pycalc.main('ceil(3.14)'), m.ceil(3.14))
        self.assertEqual(pycalc.main('copysign(-1,-2)'), m.copysign(-1, -2))
        self.assertEqual(pycalc.main('fabs(-13)'), m.fabs(-13))
        self.assertEqual(pycalc.main('factorial(5)'), m.factorial(5))
        self.assertEqual(pycalc.main('floor(3.4)'), m.floor(3.4))
        self.assertEqual(pycalc.main('fmod(5,4)'), m.fmod(5, 4))
        self.assertEqual(pycalc.main('frexp(300000)'), m.frexp(300000))
        self.assertEqual(pycalc.main('ldexp(3,10)'), m.ldexp(3, 10))
        self.assertEqual(pycalc.main('fsum([3,4,5])'), m.fsum([3, 4, 5]))
        self.assertEqual(pycalc.main('isfinite(3)'), m.isfinite(3))
        self.assertEqual(pycalc.main('isinf(3)'), m.isinf(3))
        self.assertEqual(pycalc.main('isnan(3)'), m.isnan(3))
        self.assertEqual(pycalc.main('modf(-3)'), m.modf(-3))
        self.assertEqual(pycalc.main('trunc(3.4)'), m.trunc(3.4))
        self.assertEqual(pycalc.main('exp(3)'), m.exp(3))
        self.assertEqual(pycalc.main('expm1(3)'), m.expm1(3))
        self.assertEqual(pycalc.main('log(10,2)'), m.log(10, 2))
        self.assertEqual(pycalc.main('log1p(10)'), m.log1p(10))
        self.assertEqual(pycalc.main('log10(10)'), m.log10(10))
        self.assertEqual(pycalc.main('log2(10)'), m.log2(10))
        self.assertEqual(pycalc.main('pow(2,3)'), m.pow(2, 3))
        self.assertEqual(pycalc.main('sqrt(25)'), m.sqrt(25))
        self.assertEqual(pycalc.main('erf(3)'), m.erf(3))
        self.assertEqual(pycalc.main('erfc(3)'), m.erfc(3))
        self.assertEqual(pycalc.main('gamma(3)'), m.gamma(3))
        self.assertEqual(pycalc.main('lgamma(3)'), m.lgamma(3))
        self.assertEqual(pycalc.main('gcd(1,2)'), m.gcd(1, 2))

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
        self.assertEqual(pycalc.main("100/3%2^2"), 100/3 % 2**2)

    def test_functions_and_constants(self):
        self.assertEqual(pycalc.main("pi+e"), m.pi+m.e)
        self.assertEqual(pycalc.main("log(e)"), m.log(m.e))
        self.assertEqual(pycalc.main("sin(pi/2)"), m.sin(m.pi/2))
        self.assertEqual(pycalc.main("log10(100)"), m.log10(100))
        self.assertEqual(pycalc.main("sin(pi/2)*111*6"), m.sin(m.pi/2)*111*6)
        self.assertEqual(pycalc.main("2*sin(pi/2)"), 2*m.sin(m.pi/2))

    def test_associative(self):
        self.assertEqual(pycalc.main("102%12%7"), 102 % 12 % 7)
        self.assertEqual(pycalc.main("100/4/3"), 100/4/3)
        self.assertEqual(pycalc.main("2^3^4"), 2**3**4)

    def test_comparison_operators(self):
        self.assertEqual(pycalc.main("1+2*3==1+2*3"), 1+2*3 == 1+2*3)
        self.assertAlmostEqual(pycalc.main("e^5>=e^5+1"), m.e**5 >= m.e**5+1)
        self.assertAlmostEqual(pycalc.main("1+2*4/3+1!=1+2*4/3+2"), 1+2*4/3+1 != 1+2*4/3+2)

    def test_common_tests(self):
        self.assertEqual(pycalc.main("(100)"), eval("(100)"))
        self.assertEqual(pycalc.main("666"), 666)
        self.assertEqual(pycalc.main("-.1"), -.1)
        self.assertEqual(pycalc.main("1/3"), 1/3)
        self.assertEqual(pycalc.main("1.0/3.0"), 1.0/3.0)
        self.assertEqual(pycalc.main(".1 * 2.0^56.0"), .1 * 2.0**56.0)
        self.assertEqual(pycalc.main("e^34"), m.e**34)
        self.assertEqual(pycalc.main("(2.0^(pi/pi+e/e+2.0^0.0))"),
                         (2.0**(m.pi/m.pi+m.e/m.e+2.0**0.0)))
        self.assertEqual(pycalc.main("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"),
                         (2.0**(m.pi/m.pi+m.e/m.e+2.0**0.0))**(1.0/3.0))
        self.assertEqual(pycalc.main("sin(pi/2^1) + log(1*4+2^2+1, 3^2)"),
                         m.sin(m.pi/2**1) + m.log(1*4+2**2+1, 3**2))
        self.assertEqual(pycalc.main("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"),
                         10*m.e**0*m.log10(.4 - 5 / -0.1-10) - -abs(-53/10) + -5)
        ex = "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+" \
             "cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)"
        self.assertEqual(pycalc.main(ex),
                         m.sin(-m.cos(-m.sin(3.0)-m.cos(-m.sin(-3.0*5.0)-m.sin(m.cos(m.log10(43.0))))
                                      + m.cos(m.sin(m.sin(34.0-2.0**2.0))))--m.cos(1.0)--m.cos(0.0)**3.0))
        self.assertEqual(pycalc.main("2.0^(2.0^2.0*2.0^2.0)"), 2.0**(2.0**2.0*2.0**2.0))
        self.assertEqual(pycalc.main("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"),
                         m.sin(m.e**m.log(m.e**m.e**m.sin(23.0), 45.0) +
                               m.cos(3.0+m.log10(m.e**-m.e))))


class TestEpamErrorCaseCalculator(unittest.TestCase):

    def test_unary_operators(self):
        with self.assertRaises(SystemExit):
            pycalc.main("")
        with self.assertRaises(SystemExit):
            pycalc.main("+")
        with self.assertRaises(SystemExit):
            pycalc.main("1-")
        with self.assertRaises(SystemExit):
            pycalc.main("1 2")
        with self.assertRaises(SystemExit):
            pycalc.main("ee")
        with self.assertRaises(SystemExit):
            pycalc.main("==7")
        with self.assertRaises(SystemExit):
            pycalc.main("1 + 2(3 * 4))")
        with self.assertRaises(SystemExit):
            pycalc.main("((1+2)")
        with self.assertRaises(SystemExit):
            pycalc.main("1 + 1 2 3 4 5 6")
        with self.assertRaises(SystemExit):
            pycalc.main("log100(100)")
        with self.assertRaises(SystemExit):
            pycalc.main("------")
        with self.assertRaises(SystemExit):
            pycalc.main("5 > = 6")
        with self.assertRaises(SystemExit):
            pycalc.main("5 / / 6")
        with self.assertRaises(SystemExit):
            pycalc.main("6 < = 6")
        with self.assertRaises(SystemExit):
            pycalc.main("6 * * 6")
        with self.assertRaises(SystemExit):
            pycalc.main("(((((")
        with self.assertRaises(SystemExit):
            pycalc.main("pow(2, 3, 4)")
        with self.assertRaises(SystemExit):
            pycalc.main("sqrt(-1)")
        with self.assertRaises(SystemExit):
            pycalc.main("exp(1000.0)")
