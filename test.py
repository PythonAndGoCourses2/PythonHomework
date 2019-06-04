import unittest
from operators import Operators
import split
import calc


class CalcSimpleActionsTests(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(Operators.sum(5, 9), 14)

    def test_sub(self):
        self.assertEqual(Operators.sub(11, 2), 9)

    def test_mul(self):
        self.assertEqual(Operators.mul(2, 5), 10)

    def test_div(self):
        self.assertEqual(Operators.div(8, 4), 2)

    def test_fdiv(self):
        self.assertEqual(Operators.fdiv(20, 3), 6)

    def test_less(self):
        self.assertLess(3, 4)

    def test_less_or_eql(self):
        self.assertLessEqual(5, 5)

    def test_eql(self):
        self.assertAlmostEqual(9, 9)

    def test_not_eql(self):
        self.assertNotAlmostEqual(6, 7)

    def test_gr_or_eql(self):
        self.assertGreaterEqual(10, 9)

    def test_greater(self):
        self.assertGreater(15, 1)


class CalcTestCase(unittest.TestCase):

    def test_is_num(self):
        self.assertTrue(split.is_num('11.0'))
        self.assertTrue(split.is_num('19'))
        self.assertFalse(split.is_num('a'))

    def test_split_string(self):
        s1 = '5+6/3*7'
        self.assertEqual(split.split_string(s1), ['5', '+', '6', '/', '3', '*', '7'])
        s2 = '10>=0'
        self.assertEqual(split.split_string(s2), ['10', '>=', '0'])
        s3 = 'sin(10)'
        self.assertEqual(split.split_string(s3), ['sin', '(', '10', ')'])
        s4 = 'log10(100)'
        self.assertEqual(split.split_string(s4), ['log10', '(', '100', ')'])
        s5 = '5+sin(10+5)-10^3'
        self.assertEqual(split.split_string(s5), ['5', '+', 'sin', '(', '10', '+', '5', ')', '-', '10', '^', '3'])

    def test_split_by_prefix(self):
        s = '>=+-'
        self.assertEqual(list(split.split_by_prefix(s, ['+', '-', '>=', '<=', '!=', '=='])), ['>=', '+', '-'])

    def test_tran_in_pol_not(self):
        s = '10+5^2-sin(10)'
        s2 = '5+10-60^2'
        self.assertEqual(calc.tran_in_pol_not(s), ['10', '5', '2', '^', '+', '10', 'sin', '-'])
        self.assertEqual(calc.tran_in_pol_not(s2), ['5', '10', '+', '60', '2', '^', '-'])

    def test_pols_not(self):
        s1 = ('pi', '2', '/', 'sin', '111', '*', '6', '*')
        self.assertEqual(calc.pols_not(s1), 666)
        s2 = ('1', '2', '3', '2', '*', '+', '3', '*', '+')
        self.assertEqual(calc.pols_not(s2), 25)


if __name__ == '__main__':
    unittest.main()
