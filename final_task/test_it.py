import unittest
import math
import pycalc.CheckAndChange as CheckAndChange
import pycalc.difcalc as difcalc
from unittest.mock import patch


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
        with patch('pycalc.CheckAndChange.CheckAndChange.correct_spaces'),\
                patch('pycalc.CheckAndChange.CheckAndChange.correct_brackets'), patch('pycalc.CheckAndChange.CheckAndChange.add_args'):
            self.assertEqual(
                self.cheker.do_all_changes(
                    "1122113", None), "1122113")
            with self.assertRaises(Exception):
                self.cheker.do_all_changes("", None)
                self.cheker.do_all_changes(" ", None)

    def test_module(self):
        # add other
        with self.assertRaises(Exception):
            self.cheker.add_args("module.py")

    def calculate_simple_expression(self, expr):
        return eval(expr)

    def test_comparison(self):
        with patch('pycalc.difcalc.ComplexCalc.expression_search', new=self.calculate_simple_expression):
            self.assertEqual(self.calculator.calculate(
                "12+345+664+233445+2<2"), False)
            self.assertEqual(self.calculator.calculate("12<1333<2000"), True)

            with self.assertRaises(Exception):
                self.calculator.calculate("12+345+664+233445+2<<<2")
                self.calculator.calculate("12+345+664+233445+2=2")

    def calculate_functions(self, func, expr):
        return str(eval("math." + func + "(" + expr + ")"))

    def test_funtions_search(self):
        with patch('pycalc.difcalc.ComplexCalc._find_replacement', new=self.calculate_functions), patch('pycalc.difcalc.ComplexCalc.search_brakets', new=self.calculate_simple_expression):
            self.assertAlmostEqual(
                float(
                    self.calculator.expression_search("sin(4)")),
                math.sin(4))
            self.assertAlmostEqual(
                float(
                    self.calculator.expression_search("sin(4)+1")),
                math.sin(4) + 1)
            self.assertAlmostEqual(
                float(
                    self.calculator.expression_search("pow(2,1)+13+sin(4)")), math.pow(
                    2, 1) + 13 + math.sin(4))
            with self.assertRaises(Exception):
                self.calculator.expression_search("sin(+1")
                self.calculator.expression_search("sin()+1")
                self.calculator.expression_search("pow(1)+11")
                self.assertAlmostEqual(
                    float(
                        self.calculator.expression_search("e")),
                    math.e)

    def test_function_calculator(self):
        with patch('pycalc.difcalc.ComplexCalc._commasplit') as splitted,\
                patch('pycalc.difcalc.ComplexCalc.expression_search') as expresssearch:

            splitted.return_value = ["1"]
            expresssearch.return_value = "3"
            self.assertAlmostEqual(
                float(
                    self.calculator._find_replacement(
                        "sin",
                        "1")),
                math.sin(3))

    """def test_operators(self):
        self.assertAlmostEqual(float(self.calculator.calculate("12^2")), 144.0)
        self.assertAlmostEqual(float(self.calculator.calculate("12/2")), 6.0)
        with self.assertRaises(Exception):
            self.calculator.calculate("12^`2")
            self.calculator.calculate("`12*2")
            self.calculator.calculate("12/*2")"""

    def test_unary_operators(self):
        self.assertEqual(float(self.calculator. unary_rezult("12")), 12.0)
        self.assertEqual(float(self.calculator.unary_rezult("-12")), -12.0)
        self.assertEqual(float(self.calculator.unary_rezult("+-12")), -12.0)

    def test_regulars_for_number(self):
        self.assertEqual(
            self.calculator. search_simple_number("12")[0][::-1], "12")
        self.assertEqual(self.calculator. search_simple_number(
            "12321424+2412+12")[0][::-1], "12")
        self.assertEqual(self.calculator.search_number_from_end(
            "12321424+2412+12")[0][::-1], "+12")
        self.assertEqual(self.calculator.search_number_from_end(
            "12321424+2412+--12")[0][::-1], "+--12")
        self.assertEqual(self.calculator.search_number_from_begin(
            "/12321424+2412+--12")[0], "12321424")
        self.assertEqual(self.calculator.search_number_from_begin(
            "*++-+-+12+2412+--12")[0], "++-+-+12")
        with self.assertRaises(Exception):
            self.calculator.search_number_from_begin("++-+-+12+2412+--12")
            self.calculator.search_number_from_end("12321424+2412+12/")

    def test_sum(self):
        with patch('pycalc.difcalc.ComplexCalc.unary_rezult') as number:
            number.return_value = 1
            self.assertEqual(
                self.calculator.sum("12"), 1)
            self.assertEqual(
                self.calculator.sum("12+12"), 2)

            with self.assertRaises(Exception):
                self.calculator.sum("12+*12")

    def test_brekets_parsers(self):
        pass


if __name__ == '__main__':
    # unittest.main()
    cheker = CheckAndChange.CheckAndChange()
    calculator = difcalc.ComplexCalc()

    a = "2^3^4"
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
