#!/usr/bin/env python3

import unittest
from pycalc import pycalc


class TestPycalc(unittest.TestCase):

    def test_parse_to_list_operator(self):
        self.assertEqual(pycalc.parse_to_list('><**'), ['>', '<', '*', '*'])
        self.assertEqual(pycalc.parse_to_list('>='), ['>='])

    def test_parse_to_list_int(self):
        self.assertEqual(pycalc.parse_to_list('123'), [123])

    def test_parse_to_list_float(self):
        self.assertEqual(pycalc.parse_to_list('1.23'), [1.23])
        self.assertEqual(pycalc.parse_to_list('.123'), [0.123])
        with self.assertRaises(ValueError):
            pycalc.parse_to_list('1.2.3')

    def test_parse_to_list_parentheses_comma(self):
        self.assertEqual(pycalc.parse_to_list('(,)'), ['(', ',', ')'])

    def test_parse_to_list_constant(self):
        self.assertEqual(pycalc.parse_to_list('e'), ['e'])
        self.assertEqual(pycalc.parse_to_list('e pi'), ['e', 'pi'])
        with self.assertRaises(ValueError):
            pycalc.parse_to_list('pe')

    def test_parse_to_list_func(self):
        self.assertEqual(pycalc.parse_to_list('sin(pi)'), ['sin', '(', 'pi', ')'])
        self.assertEqual(pycalc.parse_to_list('log10(10)'), ['log10', '(', 10, ')'])
        with self.assertRaises(IndexError):
            pycalc.parse_to_list('abs')
        with self.assertRaises(SyntaxError):
            pycalc.parse_to_list('abs + 1')
        with self.assertRaises(ValueError):
            pycalc.parse_to_list('abv')

    def test_parse_to_list_space(self):
        self.assertEqual(pycalc.parse_to_list('1 23'), [1, 23])

    def test_parse_to_list_else(self):
        with self.assertRaises(SyntaxError):
            pycalc.parse_to_list('&')

    def test_parse_to_list_list(self):
        self.assertIsInstance(pycalc.parse_to_list('123'), list)

    def test_parse_to_list_overall(self):
        self.assertEqual(pycalc.parse_to_list('sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))'),
                ['sin', '(', 'e', '^', 'log', '(', 'e', '^', 'e', '^', 'sin', '(', 23.0, ')', ',', 45.0, ')', '+',
                 'cos', '(', 3.0, '+', 'log10', '(', 'e', '^', '-', 'e', ')', ')', ')'])

    def test_parse_to_list_err_numbers(self):
        self.assertEqual(pycalc.parse_to_list('1 + 1 2 3 4 5 6'), [1, '+', 1, 2, 3, 4, 5, 6])

    def test_check_unary_operator_first_place(self):
        expressions = ((['-', 123], ['-u', 123]),
                             (['^', '-', 123], ['^', '-u', 123]),
                             (['(', '+', 123], ['(', '+u', 123]))
        for expression in expressions:
            pycalc.check_unary_operator(expression[0])
            self.assertEqual(expression[0], expression[1])

    def test_precedence_left(self):
        self.assertTrue(pycalc.precedence('-', '*'))
        self.assertFalse(pycalc.precedence('-', '>'))

    def test_precedence_right(self):
        self.assertFalse(pycalc.precedence('^', '-u'))

    def test_shunting_yard_alg_number(self):
        self.assertEqual(pycalc.shunting_yard_alg([123]), [123])
        self.assertEqual(pycalc.shunting_yard_alg([1.23]), [1.23])
        self.assertEqual(pycalc.shunting_yard_alg(['e']), ['e'])

    def test_check_empty_operators_empty(self):
        with self.assertRaises(SyntaxError):
            pycalc.check_empty_operators('')

    def test_check_empty_operators_false(self):
        self.assertFalse(pycalc.check_empty_operators('1'))

    def test_check_empty_operators_no_digits(self):
        with self.assertRaises(SyntaxError):
            pycalc.check_empty_operators('+')

    def test_check_brackets(self):
        self.assertTrue(pycalc.check_brackets('()()()((()))'))
        with self.assertRaises(SyntaxError):
            pycalc.check_brackets(')(')
        with self.assertRaises(SyntaxError):
            pycalc.check_brackets('()(')


if __name__ == '__main__':
    unittest.main()
