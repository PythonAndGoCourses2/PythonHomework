import unittest
import math
from src import calculate
from src import stack
from src import config


class TestMyFunctions(unittest.TestCase):

    def test_stack(self):
        self.assertIsInstance(stack.Stack(), stack.Stack)
        st = stack.Stack(0, 0, 0)
        self.assertListEqual(st.items, [0, 0, 0])
        self.assertEqual(st.pop(), 0)
        self.assertEqual(st.is_empty(), False)
        self.assertEqual(st.size(), 2)
        self.assertEqual(st.last_item(), 0)
        self.assertListEqual(st.items, [0, 0])

    def test_find_bracket(self):
        self.assertEqual(calculate.find_closing_bracket("(9ad2)"), 5)
        self.assertEqual(calculate.find_closing_bracket("((12)sad)"), 8)
        with self.assertRaises(ValueError):
            calculate.find_closing_bracket("123)")
            calculate.find_closing_bracket("((123)")
            calculate.find_closing_bracket("(123")

    def test_expression_parsing(self):
        self.assertEqual(calculate.parse_expression("12"), [12.0])
        self.assertEqual(calculate.parse_expression("12+10"), [12.0, 10.0, config.STANDART_FUNCTIONS["+"]])
        self.assertEqual(calculate.parse_expression("12+log10(10)"),
                         [12, math.log10(10), config.STANDART_FUNCTIONS["+"]])
        self.assertEqual(calculate.parse_expression("-12"), [12.0, config.STANDART_FUNCTIONS["-unary"]])
        self.assertAlmostEqual(calculate.parse_expression("log(12)"), [math.log(12)])
        with self.assertRaises(KeyError):
            calculate.parse_expression("hello 12")
            calculate.parse_expression("~12")
            calculate.parse_expression("log12")
        with self.assertRaises(ValueError):
            calculate.parse_expression("(0")
            calculate.parse_expression("0)")
            calculate.parse_expression("((0)")

    def test_regular_calculations(self):
        self.assertAlmostEqual(calculate.calculate("1+1"), 2)
        self.assertAlmostEqual(calculate.calculate("2^10"), 2**10)
        self.assertAlmostEqual(calculate.calculate("6//4"), 6 // 4)
        with self.assertRaises(KeyError):
            calculate.calculate("log(12)+*log(10)")
            calculate.calculate("(1)(2)")

    def test_functions_calculation(self):
        self.assertAlmostEqual(calculate.calculate("log(12)"), math.log(12))
        self.assertAlmostEqual(calculate.calculate("log(e, 10)"), math.log(math.e, 10))

    def test_unary_operators(self):
        self.assertAlmostEqual(calculate.calculate("-12"), -12)
        self.assertAlmostEqual(calculate.calculate("--12"), 12)
        self.assertAlmostEqual(calculate.calculate("+--+12"), 12)

    def test_logical_expressions(self):
        self.assertFalse(calculate.calculate("12==0"))
        self.assertTrue(calculate.calculate("log10(12) == " + str(math.log10(12))))


if __name__ == '__main__':
    unittest.main()
