import unittest
from ..library import Library
from .replacer import (
    replace_constant,
    replace_fanction,
    replace_brackets,
    replace_unary_operator,
    replace_bynary_operator,
    replace_compare_operator,
    replace_all_mathes
)
from ..operators import (
    MULTIPLE,
    POWER,
    TRUE_DIVISION,
    FLOOR_DIVISION,
    MODULE,
    PLUS,
    MINUS,
)


class TestReplaceFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = Library('math', 'time')

    def test_replace_constant(self):
        with self.subTest("Replaces constant name to constant value"):
            self.assertEqual(replace_constant('e', self.lib), '2.718281828459045')
            self.assertEqual(replace_constant('e + e', self.lib), '2.718281828459045 + 2.718281828459045')

        with self.subTest("Does not touch function and digit"):
            self.assertEqual(replace_constant('log()', self.lib), 'log()')
            self.assertEqual(replace_constant('log(e)', self.lib), 'log(2.718281828459045)')
            self.assertEqual(replace_constant('log(e) + e', self.lib), 'log(2.718281828459045) + 2.718281828459045')
            self.assertEqual(replace_constant('2.161727821137838e+16', self.lib), '2.161727821137838e+16')
            self.assertEqual(replace_constant('time(e) + e', self.lib), 'time(2.718281828459045) + 2.718281828459045')

    def test_replace_fanction(self):
        with self.subTest("Replaces function expression to function result"):
            self.assertEqual(replace_fanction('log10(100)', self.lib), '2.0')
            self.assertEqual(replace_fanction('log10(100) + log10(100)', self.lib), '2.0 + 2.0')
            self.assertEqual(replace_fanction('log(100,10)', self.lib), '2.0')

        with self.subTest("Does not touch constants"):
            self.assertEqual(replace_fanction('log10(100) + log(e)', self.lib), '2.0 + log(e)')
            self.assertEqual(replace_fanction('log10(100) + e', self.lib), '2.0 + e')
            self.assertEqual(replace_fanction('log10(e)', self.lib), 'log10(e)')
            self.assertEqual(replace_fanction('log10(e) + 1', self.lib), 'log10(e) + 1')

        with self.subTest("Can receive seveeral arguments"):
            self.assertEqual(replace_fanction('log(100,10)', self.lib), '2.0')
            self.assertEqual(replace_fanction('hypot(-2,0)', self.lib), '2.0')
            self.assertEqual(replace_fanction('hypot(-2,0) + log(100,10)', self.lib), '2.0 + 2.0')

    def test_replace_unary_operator(self):
        with self.subTest("Replaces sequence of unary operators"):
            self.assertEqual(replace_unary_operator('+---+1'), '-1')
            self.assertEqual(replace_unary_operator('+--+1'), '+1')
            self.assertEqual(replace_unary_operator('-13'), '-13')
            self.assertEqual(replace_unary_operator('-+---+-1'), '-1')

    def test_replace_bynary_operator(self):
        with self.subTest("Replaces sequence of bynary operators"):
            self.assertEqual(float(replace_bynary_operator('1*2*3*4', MULTIPLE)), eval('1*2*3*4'))
            self.assertEqual(float(replace_bynary_operator('2^3^4', POWER)), eval('2**3**4'))
            self.assertEqual(float(replace_bynary_operator('1/2/3/4', TRUE_DIVISION)), eval('1/2/3/4'))
            self.assertEqual(float(replace_bynary_operator('1//2//3', FLOOR_DIVISION)), eval('1//2//3'))
            self.assertEqual(float(replace_bynary_operator('1%2%3%4', MODULE)), eval('1%2%3%4'))
            self.assertEqual(float(replace_bynary_operator('1+2+3+4', PLUS)), eval('1+2+3+4'))
            self.assertEqual(float(replace_bynary_operator('1-2-3-4', MINUS)), eval('1-2-3-4'))
            self.assertEqual(float(replace_bynary_operator('-1-2-3-4', MINUS)), eval('-1-2-3-4'))

        with self.subTest("May receive several operators"):
            val = '1*2*3+1+2+3'
            self.assertEqual(float(replace_bynary_operator(val, MULTIPLE, PLUS)), eval(val))
            val = '-1-2-3-4+1+2+3+4'
            self.assertEqual(float(replace_bynary_operator(val, MINUS, PLUS)), eval(val))

    def test_replace_brackets(self):
        with self.subTest("Replaces inner brackets to result"):
            self.assertEqual(replace_brackets('(1*2*3*4)', self.lib), '+24.0')
            self.assertEqual(replace_brackets('1+(2+3*2)*3', self.lib), '1++8.0*3')
            self.assertEqual(replace_brackets('10*(2+1)', self.lib), '10*+3.0')
            self.assertEqual(replace_brackets('(100)', self.lib), '100')
            self.assertEqual(replace_brackets('(((100)))', self.lib), '((100))')

        with self.subTest("Does not touch function brakets"):
            self.assertEqual(replace_brackets('log(1*2*3*4)', self.lib), 'log(1*2*3*4)')
            self.assertEqual(replace_brackets('log((5+95),10)', self.lib), 'log(+100.0,10)')

    def test_replace_all_mathes(self):
        with self.subTest("Calculates unary operations"):
            self.assertEqual(replace_all_mathes('-13', self.lib), '-13')
            self.assertEqual(replace_all_mathes('6-(-13)', self.lib), '+19.0')
            self.assertEqual(replace_all_mathes('1---1', self.lib), '0.0')
            self.assertEqual(replace_all_mathes('-+---+-1', self.lib), '-1')

        with self.subTest("Calculates priority operations"):
            self.assertEqual(replace_all_mathes('1+2*2', self.lib), '+5.0')
            self.assertEqual(replace_all_mathes('1+(2+3*2)*3', self.lib), '+25.0')
            self.assertEqual(replace_all_mathes('10*(2+1)', self.lib), '+30.0')
            self.assertEqual(replace_all_mathes('10^(2+1)', self.lib), '+1000.0')
            self.assertEqual(replace_all_mathes('100/3^2', self.lib), '+11.11111111111111')
            self.assertEqual(replace_all_mathes('100/3%2^2', self.lib), '+1.3333333333333357')

        with self.subTest("Calculates constants and functions"):
            self.assertEqual(replace_all_mathes('pi+e', self.lib), '+5.859874482048838')
            self.assertEqual(replace_all_mathes('log(e)', self.lib), '1.0')
            self.assertEqual(replace_all_mathes('sin(pi/2)', self.lib), '1.0')
            self.assertEqual(replace_all_mathes('log10(100)', self.lib), '2.0')
            self.assertEqual(replace_all_mathes('sin(pi/2)*111*6', self.lib), '+666.0')
            self.assertEqual(replace_all_mathes('2*sin(pi/2)', self.lib), '+2.0')

        with self.subTest("Calculates assotiacive operations"):
            self.assertEqual(replace_all_mathes('102%12%7', self.lib), '+6.0')
            self.assertEqual(replace_all_mathes('100/4/3', self.lib), '+8.333333333333334')
            self.assertEqual(replace_all_mathes('2^3^4', self.lib), '+2.4178516392292583e+24')

        with self.subTest("Calculates comparation operations"):
            self.assertEqual(replace_all_mathes('1+2*3==1+2*3', self.lib), '1')
            self.assertEqual(replace_all_mathes('e^5>=e^5+1', self.lib), '0')
            self.assertEqual(replace_all_mathes('1+2*4/3+1!=1+2*4/3+2', self.lib), '1')

        with self.subTest("Calculates common operations"):
            self.assertEqual(replace_all_mathes('(100)', self.lib), '100')
            self.assertEqual(replace_all_mathes('666', self.lib), '666')
            self.assertEqual(replace_all_mathes('-.1', self.lib), '-.1')
            self.assertEqual(replace_all_mathes('1/3', self.lib), '+0.3333333333333333')
            self.assertEqual(replace_all_mathes('1.0/3.0', self.lib), '+0.3333333333333333')
            self.assertEqual(replace_all_mathes('.1*2.0^56.0', self.lib), '+7205759403792794.0')
            self.assertEqual(replace_all_mathes('e^34', self.lib), '+583461742527453.9')
            self.assertEqual(replace_all_mathes('(2.0^(pi/pi+e/e+2.0^0.0))', self.lib), '+8.0')
            self.assertEqual(replace_all_mathes('(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)', self.lib), '+2.0')
            self.assertEqual(replace_all_mathes('sin(pi/2^1)+log(1*4+2^2+1,3^2)', self.lib), '+2.0')
            self.assertEqual(replace_all_mathes('2.0^(2.0^2.0*2.0^2.0)', self.lib), '+65536.0')

            val = '10*e^0*log10(.4-5/-0.1-10)--abs(-53/10)+-5'
            self.assertEqual(replace_all_mathes(val, self.lib), '+16.36381365110605')

            val = 'sin(e^log(e^e^sin(23.0),45.0)+cos(3.0+log10(e^-e)))'
            self.assertEqual(replace_all_mathes(val, self.lib), '0.76638122986603')

            val = ('sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))'
                   '+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)')
            self.assertEqual(replace_all_mathes(val, self.lib), '0.5361064001012783')


if __name__ == '__main__':
    unittest.main()
