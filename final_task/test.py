import unittest
import pycalc
from math import *


class PycalcTest(unittest.TestCase):
    def test_check(self):
        self.assertEqual(pycalc.calculating("2+2"), 2+2)


if __name__ == '__main__':
    unittest.main()
