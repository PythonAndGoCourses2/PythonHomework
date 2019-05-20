import unittest
import math
import calc

class TestCalc(unittest.TestCase):
    """"""
    def test_errors_check(self):
        self.assertRaises(ZeroDivisionError, calc.errors_check, "12/0")
        self.assertRaises(SyntaxError, calc.errors_check, "2+-3")
        self.assertRaises(SyntaxError, calc.errors_check, "sin(1")

    def test_function_exist(self):
        self.assertRaises(NameError, calc.function_exist, ['son', '(', 1, ')'])

    def test_math_data_cheacker(self):
        self.assertIn('pi', dir(math))

    def test_solution(self):
        self.assertEqual(calc.solution('+', 5, 25), 30)
        self.assertEqual(calc.solution('-', 5, 25), -20)
        self.assertEqual(calc.solution('/', 25, 5), 5)
        self.assertEqual(calc.solution('//', 24, 5), 4)
        self.assertEqual(calc.solution('*', 2, 5.5), 11)
        self.assertEqual(calc.solution('^', 25, 2), 625)
        self.assertEqual(calc.solution('%', 26, 5), 1)

    def test_choosing_the_solution(self):
        self.assertEqual(calc.choosing_the_solution("2>=1"), True)
        self.assertEqual(calc.choosing_the_solution("2<=1"), False)
        self.assertEqual(calc.choosing_the_solution("(2+3)^2"), 25)

    def test_seperating_main_string(self):
        self.assertEqual(calc.seperating_main_string("sin(-1)"), ["sin", "(", -1, ")"])
        self.assertEqual(calc.seperating_main_string("(2.2+3.8)^2"), ["(", 2.2, "+", 3.8, ")", "^", 2])

    def test_polish_check(self):
        self.assertEqual(calc.polish_check(["(", 2.2, "+", "abs", "(", -3.8, ")", ")"]), [2.2, -3.8, "abs", "+"])
        self.assertEqual(calc.polish_check(["(", 3.2, "*", 3, "^", 2, ")", "/", "(", 7, "*", 2, ")"]),
                                           [3.2, 3, 2, "^", "*", 7, 2, "*", "/"])

    def test_count_result(self):
        self.assertEqual(calc.count_result([3.2, 3, 2, "^", "*", 7, 2, "*", "/"]), 2.0571428571428574)
        self.assertEqual(calc.count_result([2.2, -3.8, "abs", "+"]), 6)


if __name__ == '__main__':
    unittest.main()
