import unittest
import math
from math import *
import pycalc


class TestPycalc(unittest.TestCase):

    def test(self):
        self.assertEqual(pycalc.calc('2^3^4'), 2**3**4)
        self.assertEqual(pycalc.calc('sin(90)'), sin(90))
