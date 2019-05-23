import unittest
from unittest.mock import MagicMock
from calculator import validation
from calculator import calc
from time import time

from argparse import Namespace


class TestCalculator(unittest.TestCase):

    def test_result(self):
        self.assertEqual(calc.CALCULATOR('-15//2').get_result(), -15 // 2)
        self.assertEqual(calc.CALCULATOR('0-15//2').get_result(), 0 - 15 // 2)
        self.assertEqual(calc.CALCULATOR('0+15//2').get_result(), 0 + 15 // 2)
        self.assertEqual(calc.CALCULATOR('0--15//2').get_result(), 0 - -15 // 2)
        self.assertEqual(calc.CALCULATOR('0+-(-15)//2').get_result(), 0 + -(-15) // 2)

    def test_add_modules(self):
        copy_validation = validation
        args = Namespace(EXPRESSION='time()//2+20', use_modules=('time', 'math'))
        copy_validation.parse_command_line = MagicMock(return_value=args)
        expression, dicts_modules = copy_validation.check_exception()
        self.assertEqual(calc.CALCULATOR(expression, dicts_modules).get_result(), time()//2+20)


if __name__ == "__main__":
    unittest.main()
