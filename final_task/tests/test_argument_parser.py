import unittest
from unittest.mock import patch
import argparse
import math
from pycalc.argument_parser import arg_parser
from pycalc.operator_manager import create_func_dict
from pycalc.use_module_test import sin, user_function, CONSTANT, pi


class TestArgumentParser(unittest.TestCase):

    def setUp(self):
        self.func_dict = create_func_dict()

    @patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(EXPRESSION='2+40', use_modules=""))
    def test_expression_parser(self, mock_args):
        test_line = arg_parser()
        self.assertEqual(('2+40', self.func_dict), test_line)

    @patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(EXPRESSION='2+40', use_modules="use_module_test"))
    def test_expression_and_module_parser(self, mock_args):
        user_functions = {
                        'sin': sin,
                        'user_function': user_function,
                        'CONSTANT': CONSTANT,
                        'pi': pi
                        }
        func_dict = create_func_dict(user_functions)
        test_line = arg_parser()
        self.assertEqual(('2+40', func_dict), test_line)
        self.assertNotEqual(math.sin, test_line.functions['sin']['operator'])
        self.assertNotEqual(math.pi, test_line.functions['pi'])
