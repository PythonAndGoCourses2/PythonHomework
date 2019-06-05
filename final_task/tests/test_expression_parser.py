#!/usr/bin/env python3


import unittest
import math
import time

from pycalc import argument_parser, import_calc_modules, expression_parser


class TestExpressionParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        math_funcs, math_consts = import_calc_modules.import_modules(["time"])
        expression_parser.math_funcs.update(math_funcs)
        expression_parser.math_consts.update(math_consts)

    def test_are_brackets_balanced(self):
        tested_method = expression_parser._are_brackets_balanced

        self.assertTrue(tested_method("()"))
        self.assertTrue(tested_method("(1+1)"))
        self.assertTrue(tested_method("1-(1+1)"))
        self.assertTrue(tested_method("1-(1+1)+1"))

        self.assertFalse(tested_method(")("))
        self.assertFalse(tested_method("("))
        self.assertFalse(tested_method(")"))
        self.assertFalse(tested_method("(1+1))"))
        self.assertFalse(tested_method("(1-(1+1)"))

    @unittest.skip
    def test_is_number(self):
        tested_function = expression_parser._is_number

    def test_are_operators_and_operands_correct(self):
        tested_function = expression_parser._are_operators_and_operands_correct

        self.assertTrue(tested_function("1*-1"))
        self.assertTrue(tested_function("1* -1"))
        self.assertTrue(tested_function("1/ -1"))
        self.assertTrue(tested_function("1// 1"))
        self.assertTrue(tested_function("1// -1"))
        self.assertTrue(tested_function("1+.1+-1"))
        self.assertTrue(tested_function("1!=1"))
        self.assertTrue(tested_function("1<=1"))

        self.assertFalse(tested_function("1*/1"))
        self.assertFalse(tested_function("1/ /1"))
        self.assertFalse(tested_function("1// *1"))
        self.assertFalse(tested_function("1/ /*1"))
        self.assertFalse(tested_function("1-//1"))
        self.assertFalse(tested_function("1+1 1+1"))
        self.assertFalse(tested_function("1%/1"))
        self.assertFalse(tested_function("1 ! = 1"))
        self.assertFalse(tested_function("1< = 1"))
        self.assertFalse(tested_function("1 < > 1"))

        self.assertTrue(tested_function("1+pi"))
        self.assertTrue(tested_function("pi+1"))
        self.assertTrue(tested_function("log10(10)"))

        self.assertFalse(tested_function("1pi"))
        self.assertFalse(tested_function("pi1"))
        self.assertFalse(tested_function("log100(100)"))

    def test_are_no_missing_operators_next_to_brackets(self):
        tested_function = expression_parser._are_no_missing_operators_next_to_brackets

        self.assertTrue(tested_function("1+(1+1)"))
        self.assertTrue(tested_function("log10(10)"))
        self.assertTrue(tested_function("(1+1)*log10(10)"))
        self.assertTrue(tested_function("time()"))
        self.assertTrue(tested_function("log(10)"))
        self.assertTrue(tested_function("pow(2, 8)"))
        self.assertTrue(tested_function("asinh(sinh((pi+tau)/2))"))
        self.assertTrue(tested_function("sin(.5)"))
        self.assertTrue(tested_function(".5+(pi)"))

        self.assertFalse(tested_function("1(1+1)"))
        self.assertFalse(tested_function("log100(100)"))
        self.assertFalse(tested_function("(1+1)log10(10)"))
        self.assertFalse(tested_function("pi(1)"))

    @unittest.skip
    def test_remove_whitespaces(self):
        tested_function = expression_parser._remove_whitespaces

    def test_squash_doubled_plusminus(self):
        tested_function = expression_parser._squash_doubled_plusminus

        self.assertEqual(int(tested_function("-1")), eval("-1"))
        self.assertEqual(int(tested_function("---+1")), eval("---+1"))
        self.assertEqual(int(tested_function("-+--++++----+-+-+--+-1")), eval("-+--++++----+-+-+--+-1"))
        self.assertEqual(int(tested_function("-+---+-1")), eval("-+---+-1"))
        self.assertEqual(eval(tested_function("1---1")), eval("1---1"))
        self.assertEqual(eval(tested_function("-5-(-5)")), eval("-5-(-5)"))

    def test_differentiate_unary_plusminus(self):
        tested_function = expression_parser._differentiate_unary_plusminus

        self.assertEqual(tested_function("-3+1*-2"), "-#3+1*-#2")
        self.assertEqual(tested_function("+3-1//-2"), "+#3-1//-#2")
        self.assertEqual(tested_function("-1*-pow(-2+1,1-1)+sin(+pi)"), "-#1*-#pow(-#2+1,1-1)+sin(+#pi)")

    def test_bracket_exponentiation_wrapper(self):
        tested_function = expression_parser._bracket_exponentiation_wrapper

        self.assertEqual(tested_function("2^2^2^2^2"), "2^(2^(2^(2^(2))))")
        self.assertEqual(tested_function("-#2^-#2^-#2"), "-#2^(-#(2^(-#(2))))")
        self.assertEqual(tested_function("+#2^+#2^+#2"), "+#2^(+#(2^(+#(2))))")
        self.assertEqual(tested_function("1+log(-#10^5+1,10)"), "1+log(-#10^(5)+1,10)")
        self.assertEqual(tested_function("-#sin(-#pi^-#2)"), "-#sin(-#pi^(-#(2)))")

    def test_tokenizer(self):
        tested_function = expression_parser._tokenizer

        self.assertEqual(tuple(tested_function("-#pi-.10//2=>-#100")),
                         ("-#", "pi", "-", ".10", "//", "2", "=>", "-#", "100"))

        self.assertEqual(tuple(tested_function("-#2^-#2-2+1*-#1")),
                         ("-#", "2", "^", "-#", "2", "-", "2", "+", "1", "*", "-#", "1"))

        self.assertEqual(tuple(tested_function("1+2*pi-log(10,2)+10*log10(10)")),
                         ("1", "+", "2", "*", "pi", "-", "log", "(", "10", ",", "2", ")",
                          "+", "10", "*", "log10", "(", "10", ")"))

        self.assertEqual(tuple(tested_function("-#2+pi+log(100,10)-log10(+#100)")),
                         ("-#", "2", "+", "pi", "+", "log", "(", "100", ",", "10", ")",
                          "-", "log10", "(", "+#", "100", ")"))

    def test_token_handler(self):
        tested_function = expression_parser._token_handler

        self.assertEqual(tuple(tested_function(("2", "+", "2"))),
                         (2.0, 2.0, "+"))

        self.assertEqual(tuple(tested_function(("2", "/", "-#", "2"))),
                         (2.0, 2.0, "-#", "/"))

        self.assertEqual(tuple(tested_function(("2", "*", "-#", "2", "+", ".1", "*", "pi"))),
                         (2.0, 2.0, "-#", "*", 0.1, math.pi, "*", "+"))

    def test_token_handler_and_function_handler(self):
        tested_function_th = expression_parser._token_handler
        tested_function_fh = expression_parser._function_handler

        self.assertAlmostEqual(tuple(tested_function_th(("1", "+", "log10", "(", "1000", ")"))),
                               (1.0, math.log10(1000), "+"))

        self.assertLessEqual(tested_function_fh("time()"), time.time())

        self.assertAlmostEqual(tested_function_fh("log10(1000)"),
                               math.log10(1000))

        self.assertAlmostEqual(tested_function_fh("log(1000,10)"),
                               math.log(1000, 10))

        self.assertAlmostEqual(tested_function_fh("log(999+10/10,10)"),
                               math.log(999+10/10, 10))

        self.assertAlmostEqual(tested_function_fh("log((99+1),10)"),
                               math.log((99+1), 10))

    def test_polish_notation_calculate(self):
        tested_function = expression_parser._polish_notation_calculate

        self.assertAlmostEqual(tested_function((2.0, 2.0, "+")), 2+2)
        self.assertAlmostEqual(tested_function((2.0, 2.0, "-#", "^")), 2**-2)
        self.assertAlmostEqual(tested_function((2.0, 2.0, "-#", "*", 0.1, math.pi, "*", "+")),
                               2*-2+.1*math.pi)
        self.assertAlmostEqual(tested_function((2.0, 1.1, 2.3, "*", "-", 2.876, math.pi, "*", "+")),
                               2-1.1*2.3+2.876*math.pi)

    def test_calculate(self):
        tested_function = expression_parser.calculate

        self.assertAlmostEqual(tested_function("-+-+---+-1"), -+-+---+-1)
        self.assertAlmostEqual(tested_function("2+2"), 2+2)
        self.assertAlmostEqual(tested_function("-2*-10"), -2*-10)
        self.assertAlmostEqual(tested_function("-2*sin(pi)+log(100,10)-1"), -2*math.sin(math.pi)+math.log(100, 10)-1)

        self.assertAlmostEqual(tested_function("-3//2"), -3//2)  # -2
        self.assertAlmostEqual(tested_function("0-3//2"), 0-3//2)  # -1

        self.assertAlmostEqual(tested_function("-2^2"), -2**2)  # -4
        self.assertAlmostEqual(tested_function("(-2)^2"), (-2)**2)  # 4
        self.assertAlmostEqual(tested_function("2^2^2^2"), 2**2**2**2)  # 2**(2**(2**2))
        self.assertAlmostEqual(tested_function("-2^-2^-2"), -2**-2**-2)  # -(2**(-(2**-2)))

        with self.assertRaises(expression_parser.ExpressionParserError):
            tested_function("")
        with self.assertRaises(expression_parser.ExpressionParserError):
            tested_function("(1+1))")
        with self.assertRaises(expression_parser.ExpressionParserError):
            tested_function("1+2-=2")
        with self.assertRaises(expression_parser.ExpressionParserError):
            tested_function("10**10000")
        with self.assertRaises(expression_parser.ExpressionParserError):
            tested_function("1/0")
        with self.assertRaises(expression_parser.ExpressionParserError):
            tested_function("log10(100,10)")
        with self.assertRaises(expression_parser.ExpressionParserError):
            tested_function("log100(100,10)")
        with self.assertRaises(expression_parser.ExpressionParserError):
            tested_function("1+pi(10)")


if __name__ == "__main__":
    unittest.main()
