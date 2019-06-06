import unittest
from operators import *
import split
import calc


class CalcSimpleActionsTests(unittest.TestCase):

    def test_Operator(self):
        self.assertEqual(operators['+'].func(5, 9), 14)
        self.assertEqual(operators['-'].func(11, 2), 9)
        self.assertEqual(operators['*'].func(2, 5), 10)
        self.assertEqual(operators['/'].func(8, 4), 2)
        self.assertEqual(operators['//'].func(20, 3), 6)
        self.assertEqual(operators['%'].func(6, 3), 0)
        self.assertEqual(operators['^'].func(2, 3), 8)

        self.assertEqual(operators['<'].func(3, 4), True)
        self.assertEqual(operators['<='].func(5, 5), True)
        self.assertEqual(operators['=='].func(9, 9), True)
        self.assertEqual(operators['!='].func(6, 7), True)
        self.assertEqual(operators['>='].func(10, 9), True)
        self.assertEqual(operators['>'].func(15, 1), True)

    def test_priority(self):
        self.assertEqual(operators['+'].priority, 3)
        self.assertEqual(operators['-'].priority, 3)
        self.assertEqual(operators['*'].priority, 2)
        self.assertEqual(operators['/'].priority, 2)
        self.assertEqual(operators['//'].priority, 2)
        self.assertEqual(operators['%'].priority, 2)
        self.assertEqual(operators['^'].priority, 1)

        self.assertEqual(operators['<'].priority, 4)
        self.assertEqual(operators['<='].priority, 4)
        self.assertEqual(operators['=='].priority, 5)
        self.assertEqual(operators['!='].priority, 5)
        self.assertEqual(operators['>='].priority, 4)
        self.assertEqual(operators['>'].priority, 4)
        self.assertEqual(operators['!'].priority, 5)

    def test_type(self):
        self.assertEqual(operators['+'].type, 'inf')
        self.assertEqual(operators['-'].type, 'inf')
        self.assertEqual(operators['!'].type, 'post')


class SplitTests(unittest.TestCase):

    def test_is_num(self):
        self.assertTrue(split.is_num('11.0'))
        self.assertTrue(split.is_num('19'))
        self.assertFalse(split.is_num('a'))

    def test_split_string(self):
        s = '5+6/3*7'
        self.assertEqual(split.split_string(s), ['5', '+', '6', '/', '3', '*', '7'])
        s = '10>=0'
        self.assertEqual(split.split_string(s), ['10', '>=', '0'])
        s = 'sin(10)'
        self.assertEqual(split.split_string(s), ['sin', '(', '10', ')'])
        s = 'log10(100)'
        self.assertEqual(split.split_string(s), ['log10', '(', '100', ')'])
        s = '5+sin(10+5)-10^3'
        self.assertEqual(split.split_string(s), ['5', '+', 'sin', '(', '10', '+', '5', ')', '-', '10', '^', '3'])

    def test_split_by_prefix(self):
        s = '>=+-'
        self.assertEqual(list(split.split_by_prefix(s, ['+', '-', '>=', '<=', '!=', '=='])), ['>=', '+', '-'])


class PolishNotTests(unittest.TestCase):

    def test_tran_in_pol_not(self):
        s = '10+5^2-sin(10)'
        self.assertEqual(calc.tran_in_pol_not(s), ['10', '5', '2', '^', '+', '10', 'sin', '-'])
        s = '5+10-60^2'
        self.assertEqual(calc.tran_in_pol_not(s), ['5', '10', '+', '60', '2', '^', '-'])
        s = '(2.0^(pi/pi+e/e+2.0^0.0))'
        self.assertEqual(calc.tran_in_pol_not(s), ['2.0', 'pi', 'pi', '/', 'e', 'e', '/', '+', '2.0',
                                                   '0.0', '^', '+', '^'])

    def test_pols_not(self):
        s = ('pi', '2', '/', 'sin', '111', '*', '6', '*')
        self.assertEqual(calc.pols_not(s), 666)
        s = ('1', '2', '3', '2', '*', '+', '3', '*', '+')
        self.assertEqual(calc.pols_not(s), 25)
        s = ('10', '5', '2', '^', '+', '10', 'sin', '-')
        self.assertEqual(calc.pols_not(s), 35.54402111088937)
        s = ('5', '10', '+', '60', '2', '^', '-')
        self.assertEqual(calc.pols_not(s), -3585.0)


if __name__ == '__main__':
    unittest.main()
