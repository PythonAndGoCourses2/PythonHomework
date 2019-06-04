import unittest
from unittest.mock import patch
import argparse
import math
from pycalc.argument_parser import arg_parser
from pycalc.operator_manager import create_func_dict



class TestArgumentParser(unittest.TestCase):

    def setUp(self):
        self.func_dict = create_func_dict()

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(EXPRESSION='2+40', use_modules=""))
    def test_expression_parser(self, mock_args):
        test_line = arg_parser()
        self.assertEqual(('2+40', self.func_dict), test_line)
