import unittest
import core
from math import *


class PycalcTest(unittest.TestCase):
    def test_check(self):
        self.assertEqual(core.calculating("2+2"), 2+2)


if __name__ == '__main__':
    unittest.main()
