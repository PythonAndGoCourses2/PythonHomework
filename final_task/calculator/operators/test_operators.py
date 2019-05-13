import unittest
from .operators import (
    PLUS,
    MINUS,
    POWER,
    MODULE,
    MULTIPLE,
    TRUE_DIVISION,
    FLOOR_DIVISION,
    LESS,
    GREAT,
    EQUAL,
    NOT_EQUAL,
    LESS_OR_EQUAL,
    GREAT_OR_EQUAL,
    exec_operation,
)


class TestOperatorFunction(unittest.TestCase):
    def test_exec_operation(self):
        a, b = '3', '7'

        with self.subTest("Arithmetic operations return currect sting value"):
            self.assertEqual(exec_operation(a, b, MULTIPLE), '+21.0')
            self.assertEqual(exec_operation(b, a, POWER), '+2187.0')
            self.assertEqual(exec_operation(a, b, TRUE_DIVISION), '+0.42857142857142855')
            self.assertEqual(exec_operation(a, b, FLOOR_DIVISION), '0.0')
            self.assertEqual(exec_operation(a, b, MODULE), '+3.0')
            self.assertEqual(exec_operation(a, b, PLUS), '+10.0')
            self.assertEqual(exec_operation(a, b, MINUS), '-4.0')

        with self.subTest("Comparison operations return currect sting value 1 (True) or 0 (False)"):
            self.assertEqual(float(exec_operation(a, b, LESS)), a < b)
            self.assertEqual(float(exec_operation(a, b, LESS_OR_EQUAL)), a <= b)
            self.assertEqual(float(exec_operation(a, b, EQUAL)), a == b)
            self.assertEqual(float(exec_operation(a, b, NOT_EQUAL)), a != b)
            self.assertEqual(float(exec_operation(a, b, GREAT_OR_EQUAL)), a >= b)
            self.assertEqual(float(exec_operation(a, b, GREAT)), a > b)

        with self.subTest("If don't have operation throw error"):
            self.assertRaises(ValueError, lambda: exec_operation(a, b, '**'))
            self.assertRaises(ValueError, lambda: exec_operation(a, b, '&&'))
            self.assertRaises(ValueError, lambda: exec_operation(a, b, '||'))


if __name__ == '__main__':
    unittest.main()
