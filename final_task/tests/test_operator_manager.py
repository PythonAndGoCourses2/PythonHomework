import unittest
import math
from pycalc.operator_manager import create_func_dict


class TestOperatorManager(unittest.TestCase):

    def test_create_func_dict(self):
        test_func_name = dir(math) + ['round', 'abs']
        check_dict = create_func_dict()
        for key in check_dict.keys():
            self.assertTrue(key in test_func_name)
