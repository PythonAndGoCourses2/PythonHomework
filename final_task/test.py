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

    def test_parse_to_list_space(self):
        self.assertEqual(pycalc.parse_to_list('1 23'), [1, 23])

    def test_parse_to_list_else(self):
        with self.assertRaises(SyntaxError):
            pycalc.parse_to_list('&')

    def test_parse_to_list_list(self):
        self.assertIsInstance(pycalc.parse_to_list('123'), list)

    def test_precedence_left(self):
        self.assertTrue(pycalc.precedence('-', '*'))
        self.assertFalse(pycalc.precedence('-', '>'))

    def test_precedence_right(self):
        self.assertFalse(pycalc.precedence('^', '-u'))


if __name__ == '__main__':
    unittest.main()
