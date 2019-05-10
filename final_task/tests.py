import unittest
import math as m
import pycalc


class TestMyCaseCalculator(unittest.TestCase):

    def test_default_arithmetic(self):
        self.assertEqual(pycalc.py_calculator('11+11'), 11+11)
        self.assertEqual(pycalc.py_calculator('11*11'), 11*11)
        self.assertEqual(pycalc.py_calculator('11-11'), 11-11)
        self.assertEqual(pycalc.py_calculator('11/11'), 11/11)
        self.assertEqual(pycalc.py_calculator('11^2'), 11**2)
        self.assertEqual(pycalc.py_calculator('11//2'), 11//2)
        self.assertEqual(pycalc.py_calculator('11%2'), 11 % 2)

    def test_module_math_arithmetic(self):
        self.assertEqual(pycalc.py_calculator('ceil(5.11)'), m.ceil(5.11))
        self.assertEqual(pycalc.py_calculator('copysign(1, -1.0)'), m.copysign(1, -1.0))
        self.assertEqual(pycalc.py_calculator('fabs(-555)'), m.fabs(-555))
        self.assertEqual(pycalc.py_calculator('factorial(2)'), m.factorial(2))
        self.assertEqual(pycalc.py_calculator('floor(1.4)'), m.floor(1.4))
        self.assertEqual(pycalc.py_calculator('fmod(6,3)'), m.fmod(6, 3))
        self.assertEqual(pycalc.py_calculator('frexp(11000000)'), m.frexp(11000000))
        self.assertEqual(pycalc.py_calculator('ldexp(4,11)'), m.ldexp(4, 11))
        self.assertEqual(pycalc.py_calculator('fsum([1,2,3])'), m.fsum([1, 2, 3]))
        self.assertEqual(pycalc.py_calculator('gcd(5, 10)'), m.gcd(5, 10))
        self.assertEqual(pycalc.py_calculator('isclose(1, 2, rel_tol=1, abs_tol=0.0)'),
                         m.isclose(1, 2, rel_tol=1, abs_tol=0.0))
        self.assertEqual(pycalc.py_calculator('isfinite(16)'), m.isfinite(16))
        self.assertEqual(pycalc.py_calculator('isinf(16)'), m.isinf(16))
        self.assertEqual(pycalc.py_calculator('isnan(16)'), m.isnan(16))
        self.assertEqual(pycalc.py_calculator('modf(-16)'), m.modf(-16))
        self.assertEqual(pycalc.py_calculator('trunc(3.4)'), m.trunc(3.4))
        self.assertEqual(pycalc.py_calculator('exp(16)'), m.exp(16))
        self.assertEqual(pycalc.py_calculator('expm1(16)'), m.expm1(16))
        self.assertEqual(pycalc.py_calculator('log(10,2)'), m.log(10, 2))
        self.assertEqual(pycalc.py_calculator('log1p(10)'), m.log1p(10))
        self.assertEqual(pycalc.py_calculator('log10(10)'), m.log10(10))
        self.assertEqual(pycalc.py_calculator('log2(16)'), m.log2(16))
        self.assertEqual(pycalc.py_calculator('pow(2,3)'), m.pow(2, 3))
        self.assertEqual(pycalc.py_calculator('sqrt(25)'), m.sqrt(25))
        self.assertEqual(pycalc.py_calculator('erf(3)'), m.erf(3))
        self.assertEqual(pycalc.py_calculator('erfc(3)'), m.erfc(3))
        self.assertEqual(pycalc.py_calculator('gamma(3)'), m.gamma(3))
        self.assertEqual(pycalc.py_calculator('lgamma(3)'), m.lgamma(3))

    def test_module_math_trigonometry(self):
        self.assertEqual(pycalc.py_calculator('sin(90)'), m.sin(90))
        self.assertEqual(pycalc.py_calculator('cos(90)'), m.cos(90))
        self.assertEqual(pycalc.py_calculator('tan(90)'), m.tan(90))
        self.assertEqual(pycalc.py_calculator('asin(1)'), m.asin(1))
        self.assertEqual(pycalc.py_calculator('acos(0)'), m.acos(0))
        self.assertEqual(pycalc.py_calculator('atan(1)'), m.atan(1))
        self.assertEqual(pycalc.py_calculator('hypot(3,4)'), m.hypot(3, 4))
        self.assertEqual(pycalc.py_calculator('degrees(3.14)'), m.degrees(3.14))
        self.assertEqual(pycalc.py_calculator('radians(90)'), m.radians(90))
        self.assertEqual(pycalc.py_calculator('sinh(1)'), m.sinh(1))
        self.assertEqual(pycalc.py_calculator('cosh(1)'), m.cosh(1))
        self.assertEqual(pycalc.py_calculator('tanh(1)'), m.tanh(1))
        self.assertEqual(pycalc.py_calculator('asinh(1)'), m.asinh(1))
        self.assertEqual(pycalc.py_calculator('acosh(1)'), m.acosh(1))
        self.assertEqual(pycalc.py_calculator('atanh(0)'), m.atanh(0))
        self.assertEqual(pycalc.py_calculator('pi'), m.pi)
        self.assertEqual(pycalc.py_calculator('e'), m.e)
        self.assertEqual(pycalc.py_calculator('tau'), m.tau)

    def test_round_brackets(self):
        self.assertEqual(pycalc.py_calculator('(2+2)*2'), (2+2)*2)
        self.assertEqual(pycalc.py_calculator('(2+2)*2+(2+2)'), (2+2)*2+(2+2))
        self.assertEqual(pycalc.py_calculator('2+(2+(2+3)+3)+2'), 2+(2+(2+3)+3)+2)
        self.assertEqual(pycalc.py_calculator('2+(2+3)*3+2'), 2+(2+3)*3+2)
        self.assertEqual(pycalc.py_calculator('((2+2)*3)+2'), ((2+2)*3)+2)

    def test_with_floating_numbers(self):
        self.assertEqual(pycalc.py_calculator('2.3+2.3'), 2.3+2.3)
        self.assertEqual(pycalc.py_calculator('.3+0.3'), .3+0.3)
        self.assertEqual(pycalc.py_calculator('.4^-0.3'), .4**-0.3)


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
        self.assertEqual(pycalc.py_calculator("pi+e"), m.pi+m.e)
        self.assertEqual(pycalc.py_calculator("log(e)"), m.log(m.e))
        self.assertEqual(pycalc.py_calculator("sin(pi/2)"), m.sin(m.pi/2))
        self.assertEqual(pycalc.py_calculator("log10(100)"), m.log10(100))
        self.assertEqual(pycalc.py_calculator("sin(pi/2)*111*6"), m.sin(m.pi/2)*111*6)
        self.assertEqual(pycalc.py_calculator("2*sin(pi/2)"), 2*m.sin(m.pi/2))
        self.assertEqual(pycalc.py_calculator("pow(2, 3)"), m.pow(2, 3))
        self.assertEqual(pycalc.py_calculator("abs(-5)"), abs(-5))
        self.assertEqual(pycalc.py_calculator("round(123.4567890)"), round(123.4567890))

    def test_associative(self):
        self.assertEqual(pycalc.py_calculator("102%12%7"), 102 % 12 % 7)
        self.assertEqual(pycalc.py_calculator("100/4/3"), 100/4/3)
        self.assertEqual(pycalc.py_calculator("2^3^4"), 2**3**4)

    def test_comparison_operators(self):
        self.assertEqual(pycalc.py_calculator("1+2*3==1+2*3"), 1+2*3 == 1+2*3)
        self.assertAlmostEqual(pycalc.py_calculator("e^5>=e^5+1"), m.e**5 >= m.e**5+1)
        self.assertAlmostEqual(pycalc.py_calculator("1+2*4/3+1!=1+2*4/3+2"), 1+2*4/3+1 != 1+2*4/3+2)

    def test_common_tests(self):
        self.assertEqual(pycalc.py_calculator("(100)"), eval("(100)"))
        self.assertEqual(pycalc.py_calculator("666"), 666)
        self.assertEqual(pycalc.py_calculator("-.1"), -.1)
        self.assertEqual(pycalc.py_calculator("1/3"), 1/3)
        self.assertEqual(pycalc.py_calculator("1.0/3.0"), 1.0/3.0)
        self.assertEqual(pycalc.py_calculator(".1 * 2.0^56.0"), .1 * 2.0**56.0)
        self.assertEqual(pycalc.py_calculator("e^34"), m.e**34)
        self.assertEqual(pycalc.py_calculator("(2.0^(pi/pi+e/e+2.0^0.0))"),
                         (2.0**(m.pi/m.pi+m.e/m.e+2.0**0.0)))
        self.assertEqual(pycalc.py_calculator("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"),
                         (2.0**(m.pi/m.pi+m.e/m.e+2.0**0.0))**(1.0/3.0))
        self.assertEqual(pycalc.py_calculator("sin(pi/2^1) + log(1*4+2^2+1, 3^2)"),
                         m.sin(m.pi/2**1) + m.log(1*4+2**2+1, 3**2))
        self.assertEqual(pycalc.py_calculator("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"),
                         10*m.e**0*m.log10(.4 - 5 / -0.1-10) - -abs(-53/10) + -5)
        ex = "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+" \
             "cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)"
        self.assertEqual(pycalc.py_calculator(ex),
                         m.sin(-m.cos(-m.sin(3.0)-m.cos(-m.sin(-3.0*5.0)-m.sin(m.cos(m.log10(43.0))))
                                      + m.cos(m.sin(m.sin(34.0-2.0**2.0))))--m.cos(1.0)--m.cos(0.0)**3.0))
        self.assertEqual(pycalc.py_calculator("2.0^(2.0^2.0*2.0^2.0)"), 2.0**(2.0**2.0*2.0**2.0))
        self.assertEqual(pycalc.py_calculator("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"),
                         m.sin(m.e**m.log(m.e**m.e**m.sin(23.0), 45.0) + m.cos(3.0+m.log10(m.e**-m.e))))

    def test_error_cases(self):
        self.assertRaises(ValueError, pycalc.py_calculator, "")
        self.assertRaises(ValueError, pycalc.py_calculator, "+")
        self.assertRaises(ValueError, pycalc.py_calculator, "1-")
        self.assertRaises(ValueError, pycalc.py_calculator, "1 2")
        self.assertRaises(ValueError, pycalc.py_calculator, "ee")
        self.assertRaises(ValueError, pycalc.py_calculator, "1 + 2(3 * 4))")
        self.assertRaises(ValueError, pycalc.py_calculator, "((1+2)")
        self.assertRaises(ValueError, pycalc.py_calculator, "1 + 1 2 3 4 5 6")
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
