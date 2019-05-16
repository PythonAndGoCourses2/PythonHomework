import unittest
import pycalc
from math import *


class PycalcTest(unittest.TestCase):
    def test_check(self):
        self.assertEqual(pycalc.calculating("pi+e"), pi + e)
        self.assertEqual(pycalc.calculating("(2.0^(pi/pi+e/e+2.0^0.0))"), (2.0 ** (pi / pi + e / e + 2.0 ** 0.0)))
        self.assertEqual(pycalc.calculating("(2.0^(pi/pi+e/e+2.0^0.0))"), (2.0 ** (pi / pi + e / e + 2.0 ** 0.0)))


if __name__ == '__main__':
    unittest.main()
