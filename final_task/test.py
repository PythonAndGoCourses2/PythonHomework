import unittest
import math
import pycalc


class TestMyCaseCalculator(unittest.TestCase):

    def test_default_arithmetic(self):
        self.assertEqual(pycalc.main('2+2'), eval('2+2'))
        self.assertEqual(pycalc.main('2*2'), eval('2*2'))
        self.assertEqual(pycalc.main('2-2'), eval('2-2'))
        self.assertEqual(pycalc.main('2/2'), eval('2/2'))
        self.assertEqual(pycalc.main('2^2'), eval('2**2'))
        self.assertEqual(pycalc.main('2//2'), eval('2//2'))
        self.assertEqual(pycalc.main('2%2'), eval('2%2'))

    def test_more_than_one_number(self):
        self.assertEqual(pycalc.main('22+22'), eval('22+22'))
        self.assertEqual(pycalc.main('222+222'), eval('222+222'))

    def test_module_math_trigonometry(self):
        self.assertEqual(pycalc.main('sin(90)'), eval('math.sin(90)'))
        self.assertEqual(pycalc.main('cos(90)'), eval('math.cos(90)'))
        self.assertEqual(pycalc.main('tan(90)'), eval('math.tan(90)'))
        self.assertEqual(pycalc.main('asin(1)'), eval('math.asin(1)'))
        self.assertEqual(pycalc.main('acos(0)'), eval('math.acos(0)'))
        self.assertEqual(pycalc.main('atan(1)'), eval('math.atan(1)'))
        self.assertEqual(pycalc.main('hypot(3,4)'), eval('math.hypot(3,4)'))
        self.assertEqual(pycalc.main('degrees(3.14)'), eval('math.degrees(3.14)'))
        self.assertEqual(pycalc.main('radians(90)'), eval('math.radians(90)'))
        self.assertEqual(pycalc.main('sinh(1)'), eval('math.sinh(1)'))
        self.assertEqual(pycalc.main('cosh(1)'), eval('math.cosh(1)'))
        self.assertEqual(pycalc.main('tanh(1)'), eval('math.tanh(1)'))
        self.assertEqual(pycalc.main('asinh(1)'), eval('math.asinh(1)'))
        self.assertEqual(pycalc.main('acosh(1)'), eval('math.acosh(1)'))
        self.assertEqual(pycalc.main('atanh(0)'), eval('math.atanh(0)'))
        self.assertEqual(pycalc.main('pi'), eval('math.pi'))

    def test_module_math_arithmetic(self):
        self.assertEqual(pycalc.main('ceil(3.14)'), eval('math.ceil(3.14)'))
        self.assertEqual(pycalc.main('copysign(-1,-2)'), eval('math.copysign(-1,-2)'))
        self.assertEqual(pycalc.main('fabs(-13)'), eval('math.fabs(-13)'))
        self.assertEqual(pycalc.main('factorial(5)'), eval('math.factorial(5)'))
        self.assertEqual(pycalc.main('floor(3.4)'), eval('math.floor(3.4)'))
        self.assertEqual(pycalc.main('fmod(5,4)'), eval('math.fmod(5,4)'))
        self.assertEqual(pycalc.main('frexp(300000)'), eval('math.frexp(300000)'))
        self.assertEqual(pycalc.main('ldexp(3,10)'), eval('math.ldexp(3,10)'))
        self.assertEqual(pycalc.main('fsum([3,4,5])'), eval('math.fsum([3,4,5])'))
        self.assertEqual(pycalc.main('isfinite(3)'), eval('math.isfinite(3)'))
        self.assertEqual(pycalc.main('isinf(3)'), eval('math.isinf(3)'))
        self.assertEqual(pycalc.main('isnan(3)'), eval('math.isnan(3)'))
        self.assertEqual(pycalc.main('modf(-3)'), eval('math.modf(-3)'))
        self.assertEqual(pycalc.main('trunc(3.4)'), eval('math.trunc(3.4)'))
        self.assertEqual(pycalc.main('exp(3)'), eval('math.exp(3)'))
        self.assertEqual(pycalc.main('expm1(3)'), eval('math.expm1(3)'))
        self.assertEqual(pycalc.main('log(10,2)'), eval('math.log(10,2)'))
        self.assertEqual(pycalc.main('log1p(10)'), eval('math.log1p(10)'))
        self.assertEqual(pycalc.main('log10(10)'), eval('math.log10(10)'))
        self.assertEqual(pycalc.main('log2(10)'), eval('math.log2(10)'))
        self.assertEqual(pycalc.main('pow(2,3)'), eval('math.pow(2,3)'))
        self.assertEqual(pycalc.main('sqrt(25)'), eval('math.sqrt(25)'))
        self.assertEqual(pycalc.main('erf(3)'), eval('math.erf(3)'))
        self.assertEqual(pycalc.main('erfc(3)'), eval('math.erfc(3)'))
        self.assertEqual(pycalc.main('gamma(3)'), eval('math.gamma(3)'))
        self.assertEqual(pycalc.main('lgamma(3)'), eval('math.lgamma(3)'))

    def test_round_brackets(self):
        self.assertEqual(pycalc.main('(2+2)*2'), eval('(2+2)*2'))
        self.assertEqual(pycalc.main('(2+2)*2+(2+2)'), eval('(2+2)*2+(2+2)'))
        self.assertEqual(pycalc.main('2+(2+(2+3)+3)+2'), eval('2+(2+(2+3)+3)+2'))
        self.assertEqual(pycalc.main('2+(2+3)*3+2'), eval('2+(2+3)*3+2'))
        self.assertEqual(pycalc.main('((2+2)*3)+2'), eval('((2+2)*3)+2'))

    def test_with_floating_numbers(self):
        self.assertEqual(pycalc.main('2.3+2.3'), eval('2.3+2.3'))


class TestEpamCaseCalculator(unittest.TestCase):

    def test_unary_operators(self):
        self.assertEqual(pycalc.main("-13"), eval("-13"))
        self.assertEqual(pycalc.main("6-(-13)"), eval("6-(-13)"))
        self.assertEqual(pycalc.main("1---1"), eval("1---1"))
        self.assertEqual(pycalc.main("-+---+-1"), eval("-+---+-1"))

    def test_operation_priority(self):
        self.assertEqual(pycalc.main("1+2*2"), eval("1+2*2"))
        self.assertEqual(pycalc.main("1+(2+3*2)*3"), eval("1+(2+3*2)*3"))
        self.assertEqual(pycalc.main("10*(2+1)"), eval("10*(2+1)"))
        self.assertEqual(pycalc.main("10^(2+1)"), eval("10**(2+1)"))
        self.assertEqual(pycalc.main("100/3^2"), eval("100/3**2"))
        self.assertEqual(pycalc.main("100/3%2^2"), eval("100/3%2**2"))

    def test_functions_and_constants(self):
        self.assertEqual(pycalc.main("pi+e"), eval("math.pi+math.e"))
        self.assertEqual(pycalc.main("log(e)"), eval("math.log(math.e)"))
        self.assertEqual(pycalc.main("sin(pi/2)"), eval("math.sin(math.pi/2)"))
        self.assertEqual(pycalc.main("log10(100)"), eval("math.log10(100)"))
        self.assertEqual(pycalc.main("sin(pi/2)*111*6"), eval("math.sin(math.pi/2)*111*6"))
        self.assertEqual(pycalc.main("2*sin(pi/2)"), eval("2*math.sin(math.pi/2)"))

    def test_associative(self):
        self.assertEqual(pycalc.main("102%12%7"), eval("102%12%7"))
        self.assertEqual(pycalc.main("100/4/3"), eval("100/4/3"))
        self.assertEqual(pycalc.main("2^3^4"), eval("2**3**4"))

    # def test_comparison_operators(self):
    #     self.assertEqual(pycalc.main("1+2*3==1+2*3"), eval("1+2*3==1+2*3"))
    #     self.assertEqual(pycalc.main("e^5>=e^5+1"), eval("e**5>=e**5+1"))
    #     self.assertEqual(pycalc.main("1+2*4/3+1!=1+2*4/3+2"), eval("1+2*4/3+1!=1+2*4/3+2"))

    def test_common_tests(self):
        self.assertEqual(pycalc.main("(100)"), eval("(100)"))
        self.assertEqual(pycalc.main("666"), eval("666"))
        self.assertEqual(pycalc.main("-.1"), eval("-.1"))
        self.assertEqual(pycalc.main("1/3"), eval("1/3"))
        self.assertEqual(pycalc.main("1.0/3.0"), eval("1.0/3.0"))
        self.assertEqual(pycalc.main(".1 * 2.0^56.0"), eval(".1 * 2.0**56.0"))
        self.assertEqual(pycalc.main("e^34"), eval("math.e**34"))
        self.assertEqual(pycalc.main("(2.0^(pi/pi+e/e+2.0^0.0))"), eval("(2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))"))
        self.assertEqual(pycalc.main("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"), eval("(2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))**(1.0/3.0)"))
        self.assertEqual(pycalc.main("sin(pi/2^1) + log(1*4+2^2+1, 3^2)"), eval("math.sin(math.pi/2**1) + math.log(1*4+2**2+1, 3**2)"))
        self.assertEqual(pycalc.main("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"), eval("10*math.e**0*math.log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"))
        self.assertEqual(pycalc.main("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)"), eval("math.sin(-math.cos(-math.sin(3.0)-math.cos(-math.sin(-3.0*5.0)-math.sin(math.cos(math.log10(43.0))))+math.cos(math.sin(math.sin(34.0-2.0**2.0))))--math.cos(1.0)--math.cos(0.0)**3.0)"))
        self.assertEqual(pycalc.main("2.0^(2.0^2.0*2.0^2.0)"), eval("2.0**(2.0**2.0*2.0**2.0)"))
        self.assertEqual(pycalc.main("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"), eval("math.sin(math.e**math.log(math.e**math.e**math.sin(23.0),45.0) + math.cos(3.0+math.log10(math.e**-math.e)))"))
