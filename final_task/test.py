import unittest
from math import *
import check


class TestCheckFunctions(unittest.TestCase):
    def test_brackets_check(self):
        self.assertEqual(check.brackets_check('()'), True)
        self.assertEqual(check.brackets_check('(()'), False)
        self.assertEqual(check.brackets_check(''), True)

    def test_comparison_check(self):
        self.assertEqual(check.comparison_check("5>2"), ">")
        self.assertEqual(check.comparison_check("10<12"), "<")
        self.assertEqual(check.comparison_check("2+2<=5+6"), "<=")
        self.assertEqual(check.comparison_check("12>=5+6"), ">=")
        self.assertEqual(check.comparison_check("7+3==8+2"), "==")
        self.assertEqual(check.comparison_check("10!=2+3*5"), "!=")
        self.assertEqual(check.comparison_check("10+3*(2+1)"), False)
        self.assertEqual(check.comparison_check("5-2"), False)

    def test_comparison_calc(self):
        self.assertEqual(check.comparison_calc("5>2", ">"), True)
        self.assertEqual(check.comparison_calc("5+2<20+1", "<"), True)
        self.assertEqual(check.comparison_calc("5^2>=2+2", ">="), True)
        self.assertEqual(check.comparison_calc("5^3<=2+3*(1+2)", "<="), False)
        self.assertEqual(check.comparison_calc("5==2", "=="), False)
        self.assertEqual(check.comparison_calc("8+2!=7+3", "!="), False)

    def test_fix_unary(self):
        self.assertEqual(check.fix_unary("-2+3"), "0-2+3")
        self.assertEqual(check.fix_unary("0+3/3"), "0+3/3")
        self.assertEqual(check.fix_unary("2+3*(-1+2)"), "2+3*(0-1+2)")
        self.assertEqual(check.fix_unary("2+30*(+1+2)"), "2+30*(0+1+2)")

    def test_replace_plus_minus(self):
        self.assertEqual(check.replace_plus_minus("2+++3"), "2+3")
        self.assertEqual(check.replace_plus_minus("2++++4"), "2+4")
        self.assertEqual(check.replace_plus_minus("2/3-----.5"), "2/3-.5")
        self.assertEqual(check.replace_plus_minus("2.0----6"), "2.0+6")
        self.assertEqual(check.replace_plus_minus("2+-+-7"), "2+7")
        self.assertEqual(check.replace_plus_minus("2+--+-8"), "2-8")
        self.assertEqual(check.replace_plus_minus("2-+++--+9"), "2-9")
        self.assertEqual(check.replace_plus_minus("--+-2.0-+--10"), "-2.0-10")

    def test_replace_whitespace_and_const(self):
        self.assertEqual(check.replace_whitespace_and_const("3 +  4"), "3+4")
        self.assertEqual(check.replace_whitespace_and_const("3+ 4 *    (5 + 2 / 10 ) "), "3+4*(5+2/10)")
        self.assertEqual(check.replace_whitespace_and_const("2+e/pi"), "2+{0}/{1}".format(e, pi))
        self.assertEqual(check.replace_whitespace_and_const("10*tau+e^e"), "10*{tau}+{e}^{e}".format(tau=tau, e=e))
        self.assertEqual(check.replace_whitespace_and_const("2+inf-nan"), "2+{0}-{1}".format(inf, nan))

    def test_correct_check(self):
        self.assertEqual(check.correct_check("1+2^3"), "1+2^3")
        self.assertEqual(check.correct_check("5//2"), "5//2")
        self.assertEqual(check.correct_check("1/2*3^4%5"), "1/2*3^4%5")
        self.assertEqual(check.correct_check("1+2*3-"), False)
        self.assertEqual(check.correct_check("1+2*3*"), False)
        self.assertEqual(check.correct_check("1 2 "), False)
        self.assertEqual(check.correct_check("1 ^ ^ 5"), False)
        self.assertEqual(check.correct_check("1 * * 6"), False)
        self.assertEqual(check.correct_check("1 / / 7"), False)
        self.assertEqual(check.correct_check("1 % % 8"), False)


if __name__ == '__main__':
    unittest.main()
