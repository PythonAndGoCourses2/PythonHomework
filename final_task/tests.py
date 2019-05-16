import unittest
import math
import pycalc.CheckAndChange as CheckAndChange
import pycalc.difcalc as difcalc


class TestFunctions(unittest.TestCase):

    cheker = CheckAndChange.CheckAndChange()
    calculator = difcalc.ComplexCalc()

    def test_brackets(self):
        self.assertEqual(self.cheker.correct_brackets("(()())"), None)
        with self.assertRaises(Exception):
            self.cheker.correct_brackets("(()()")
            self.cheker.correct_brackets("())")
            self.cheker.correct_brackets(")(")

    def test_space_cheker(self):
        self.assertEqual(self.cheker.correct_spaces("1*2"), None)
        self.assertEqual(self.cheker.correct_spaces("1 * 2"), None)
        with self.assertRaises(Exception):
            self.cheker.correct_spaces("1 2*2")
            self.cheker.correct_spaces("12 * * 2")

    def test_numbers(self):
        self.assertEqual(
            self.cheker.do_all_changes(
                "1122113", None), "1122113")
        with self.assertRaises(Exception):
            self.cheker.do_all_changes("", None)
            self.cheker.do_all_changes(" ", None)

    def test_module(self):

        with self.assertRaises(Exception):
            self.cheker.add_args("module.py")

    def test_comparison(self):
        self.assertEqual(self.calculator.calculate(
            "12+345+664+233445+2<2"), False)

        with self.assertRaises(Exception):
            self.calculator.calculate("12+345+664+233445+2<<<2")
            self.calculator.calculate("12+345+664+233445+2=2")

    def test_operators(self):
        self.assertAlmostEqual(float(self.calculator.calculate("12^2")), 144.0)
        self.assertAlmostEqual(float(self.calculator.calculate("12/2")), 6.0)
        with self.assertRaises(Exception):
            self.calculator.calculate("12^`2")
            self.calculator.calculate("`12*2")
            self.calculator.calculate("12/*2")

    def test_funtions(self):
        self.assertAlmostEqual(
            float(
                self.calculator.calculate("sin(4)")),
            math.sin(4))
        self.assertAlmostEqual(
            float(
                self.calculator.calculate("pow(2,1)")), math.pow(
                2, 1))
        with self.assertRaises(Exception):
            self.calculator.calculate("sin()")
            self.calculator.calculate("pow(1)")

    def test_constants(self):
        self.assertAlmostEqual(float(self.calculator.calculate("e")), math.e)


if __name__ == '__main__':
    calculator = difcalc.ComplexCalc()
    cheker = CheckAndChange. CheckAndChange()
    unittest.main()
"""
    a="13+2"
    try:

        if a != "--help":

            a = cheker.do_all_changes(a, None)
            a = calculator.calculate(a)

        else:
            print("help yourself")

    except Exception as e:
        print("ERROR:  " + str(e))
    else:
        print(a)
    """
