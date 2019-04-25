import unittest
from PythonHomework.final_task.pycalc.core import calculator


class TestCalculator(unittest.TestCase):
    def test_solve(self):
        self.assertEqual(calculator.solve('110 * 180 +(360 - 200 + (3 - 2))'), 19961.0)
