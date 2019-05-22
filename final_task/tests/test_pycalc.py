import unittest
from pycalc.pycalc import main
from pycalc.calculator import Calculator


class TestPycalc(unittest.TestCase):

    def test_calc(self):
        test_expression = 'round(-2+(tau^2-sin(pi/2)*2+6.5))'
        calc = Calculator(test_expression)
        self.assertEqual(42, calc.calculate())

    def test_syntax_error_in_init_class(self):
        test_expression = '15*'
        with self.assertRaises(SyntaxError):
            Calculator(test_expression)

    def test_syntax_error_in_class_method(self):
        test_expression = 'sin(pi, 45)'
        calc = Calculator(test_expression)
        with self.assertRaises(SyntaxError):
            calc.calculate()

    def test_zero_division_error(self):
        test_expression = '42/0'
        calc = Calculator(test_expression)
        with self.assertRaises(ZeroDivisionError):
            calc.calculate()

    def test_math_error(self):
        test_expression = 'sqrt(-10)'
        calc = Calculator(test_expression)
        with self.assertRaises(ValueError):
            calc.calculate()

    def test_overflow_error(self):
        test_expression = 'exp(1000.0)'
        calc = Calculator(test_expression)
        with self.assertRaises(OverflowError):
            calc.calculate()
