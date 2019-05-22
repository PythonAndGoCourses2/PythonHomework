import unittest
import math


def create_func_dict():
    func_dict = {
                'abs': {'operator': abs, 'priority': 0},
                'round': {'operator': round, 'priority': 0}
                }
    for k, v in math.__dict__.items():
        if k.startswith('_'):
            continue
        func_dict[k] = {'operator': v, 'priority': 0}
    return func_dict

class TestOperatorManager(unittest.TestCase):

    def test_create_func_dict(self):
        test_func_name = dir(math) + ['round', 'abs']
        check_dict = create_func_dict()
        for key in check_dict.keys():
            self.assertTrue(key in test_func_name)

