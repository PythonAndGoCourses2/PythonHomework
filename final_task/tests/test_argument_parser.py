import unittest
from unittest import mock
import argparse
from pycalc.argument_parser import arg_parser
from pycalc.operator_manager import create_func_dict


class TestArgumentParser(unittest.TestCase):

    def setUp(self):
        self.fucn_dict = create_func_dict()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(EXPRESSION='2+40', use_modules=""))
    def test_expression_parser(self):
        test_line = arg_parser()
        self.assertEqual(('2+40', self.func_dict), test_line)
