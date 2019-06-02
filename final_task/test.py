import unittest
import math
import check
import core


class TestCheckFunctions(unittest.TestCase):
    def test_brackets_check(self):
        self.assertTrue(check.brackets_check('()'))
        self.assertFalse(check.brackets_check('(()'))
        self.assertTrue(check.brackets_check(''))
        self.assertFalse(check.brackets_check(')()'))

    def test_comparison_check(self):
        self.assertEqual(check.comparison_check("5>2"), ">")
        self.assertEqual(check.comparison_check("10<12"), "<")
        self.assertEqual(check.comparison_check("2+2<=5+6"), "<=")
        self.assertEqual(check.comparison_check("12>=5+6"), ">=")
        self.assertEqual(check.comparison_check("7+3==8+2"), "==")
        self.assertEqual(check.comparison_check("10!=2+3*5"), "!=")
        self.assertFalse(check.comparison_check("10+3*(2+1)"))
        self.assertFalse(check.comparison_check("5-2"))

    def test_comparison_calc(self):
        self.assertTrue(check.comparison_calc("5>2", ">"))
        self.assertTrue(check.comparison_calc("5+2<20+1", "<"))
        self.assertTrue(check.comparison_calc("5^2>=2+2", ">="))
        self.assertFalse(check.comparison_calc("5^3<=2+3*(1+2)", "<="))
        self.assertFalse(check.comparison_calc("5==2", "=="))
        self.assertFalse(check.comparison_calc("8+2!=7+3", "!="))
        # should add test for exit(-1)

    def test_fix_unary(self):
        self.assertEqual(check.fix_unary("-2+3"), "0-2+3")
        self.assertEqual(check.fix_unary("0+3/3"), "0+3/3")
        self.assertEqual(check.fix_unary("2+3*(-1+2)"), "2+3*(0-1+2)")
        self.assertEqual(check.fix_unary("2+30*(+1+2)"), "2+30*(0+1+2)")
        self.assertEqual(check.fix_unary("2+3*(4+5)"), "2+3*(4+5)")

    def test_replace_plus_minus(self):
        self.assertEqual(check.replace_plus_minus("2+++3"), "2+3")
        self.assertEqual(check.replace_plus_minus("2++++4"), "2+4")
        self.assertEqual(check.replace_plus_minus("2/3-----.5"), "2/3-.5")
        self.assertEqual(check.replace_plus_minus("2.0----6"), "2.0+6")
        self.assertEqual(check.replace_plus_minus("2+-+-7"), "2+7")
        self.assertEqual(check.replace_plus_minus("2-+-+8"), "2+8")
        self.assertEqual(check.replace_plus_minus("2-+++--+9"), "2-9")
        self.assertEqual(check.replace_plus_minus("--+-2.0-+--10"), "-2.0-10")
        self.assertEqual(check.replace_plus_minus("2*2/3"), "2*2/3")

    def test_replace_whitespace_and_const(self):
        self.assertEqual(check.replace_whitespace_and_const("3 +  4"), "3+4")
        self.assertEqual(check.replace_whitespace_and_const("3+ 4 *    (5 + 2 / 10 ) "), "3+4*(5+2/10)")
        self.assertEqual(check.replace_whitespace_and_const("e+1"), "{}+1".format(math.e))
        self.assertEqual(check.replace_whitespace_and_const("2+e/pi"), "2+{0}/{1}".format(math.e, math.pi))
        self.assertEqual(check.replace_whitespace_and_const("2*tau^e"), "2*{tau}^{e}".format(tau=math.tau, e=math.e))
        self.assertEqual(check.replace_whitespace_and_const("2+inf-nan"), "2+{0}-{1}".format(math.inf, math.nan))

    def test_common_check(self):
        self.assertEqual(check.common_check("1 + 2 ^  3"), "1 + 2 ^  3")
        self.assertEqual(check.common_check("5//2"), "5//2")
        self.assertEqual(check.common_check("1/2*3^4%5"), "1/2*3^4%5")
        self.assertFalse(check.common_check("1+2*3+"))
        self.assertFalse(check.common_check("1+2*3-"))
        self.assertFalse(check.common_check("1+2*3*"))
        self.assertFalse(check.common_check("1+2*3/"))
        self.assertFalse(check.common_check("1+2*3//"))
        self.assertFalse(check.common_check("1+2*3%"))
        self.assertFalse(check.common_check("1+2*3^"))
        self.assertFalse(check.common_check("1 2 "))
        self.assertFalse(check.common_check("1 ^ ^ 5"))
        self.assertFalse(check.common_check("1 * * 6"))
        self.assertFalse(check.common_check("1 / / 7"))
        self.assertFalse(check.common_check("1 % % 8"))

    def test_check_arg_function(self):
        self.assertEqual(check.check_arg_function("log(8,2)+sin(3)"), "log(8,2)+sin(3)")
        self.assertFalse(check.check_arg_function("sin(2,3,4)"))
        self.assertEqual(check.check_arg_function("2+2"), "2+2")


class TestCoreFunctions(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(core.parse("1+2"), [1, "+", 2])
        self.assertEqual(core.parse("1^2^3"), [1, "^", 2, "^", 3])
        self.assertEqual(core.parse("log2(8)"), [3])
        self.assertEqual(core.parse("log(16,2)"), [4])
        self.assertEqual(core.parse("abs(5)"), [5])
        self.assertEqual(core.parse("log10(2*(52-2))"), [2])
        self.assertEqual(core.parse("1.0/2.0"), [1.0, "/", 2.0])
        self.assertEqual(core.parse("10//2"), [10, "//", 2])

    def test_math_function_calculating(self):
        self.assertEqual(core.math_function_calculating(math.log, "8,2"), 3)
        self.assertEqual(core.math_function_calculating(math.sin, "2"), math.sin(2))

    def test_comma_count(self):
        self.assertEqual(core.comma_count(math.log), 1)
        self.assertEqual(core.comma_count(math.sin), 0)
        self.assertEqual(core.comma_count(round), 1)
        self.assertEqual(core.comma_count(abs), 0)

    def test_infix_to_postfix(self):
        self.assertEqual(core.infix_to_postfix([2, "^", 3]), [2, 3, "^"])
        self.assertEqual(core.infix_to_postfix([2, "^", 2, "^", 3]), [2, 2, 3, "^", "^"])
        self.assertEqual(core.infix_to_postfix([2, "*", '(', 3, "+", 2, ")"]), [2, 3, 2, "+", "*"])
        self.assertEqual(core.infix_to_postfix([2, "^", 3]), [2, 3, "^"])
        self.assertEqual(core.infix_to_postfix([]), [])

    def test_calc(self):
        self.assertEqual(core.calc([2, 3, "+"]), 5)
        self.assertEqual(core.calc([5]), 5)
        self.assertEqual(core.calc([2, 3, 5, "*", "+"]), 17)


if __name__ == '__main__':
    unittest.main()
