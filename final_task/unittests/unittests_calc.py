# -*- coding: Windows-1251 -*-
import unittest
import math

from final_task.pycalc_proc import PyCalcProcessing

calc_obj = PyCalcProcessing('1')


class TestCalcing(unittest.TestCase):

    # Unary operators
    def test1(self):
        self.assertEqual(-13.0, calc_obj.calc([0.0, 13.0, '-']))

    def test2(self):
        self.assertEqual(6.0 - (-13.0), calc_obj.calc([6.0, 0.0, 13.0, '-', '-']))

    def test3(self):
        self.assertEqual(1.0---1.0, calc_obj.calc([1.0, 1.0, '-']))

    def test4(self):
        self.assertEqual(-+---+-1.0, calc_obj.calc([0.0, 1.0, '-']))

    def test5(self):
        self.assertEqual(1.0 + 2.0 * 2.0, calc_obj.calc([1.0, 2.0, 2.0, '*', '+']))

    def test6(self):
        self.assertEqual(1.0 + (2.0 + 3.0 * 2.0) * 3.0, calc_obj.calc([1.0, 2.0, 3.0, 2.0, '*', '+', 3.0, '*', '+']))

    def test7(self):
        self.assertEqual(10.0 * (2.0 + 1.0), calc_obj.calc([10.0, 2.0, 1.0, '+', '*']))

    def test8(self):
        self.assertEqual(10.0 ** (2.0 + 1.0), calc_obj.calc([10.0, 2.0, 1.0, '+', '^']))

    def test9(self):
        self.assertEqual(100.0 / 3.0 ** 2.0, calc_obj.calc([100.0, 3.0, 2.0, '^', '/']))

    def test10(self):
        self.assertEqual(100.0 / 3.0 % 2.0 ** 2.0, calc_obj.calc([100.0, 3.0, '/', 2.0, 2.0, '^', '%']))

    # Functions and constants
    def test11(self):
        self.assertEqual(math.pi + math.e, calc_obj.calc(['pi', 'e', '+']))

    def test12(self):
        self.assertEqual(math.log(math.e), calc_obj.calc(['e', 'log']))

    def test13(self):
        self.assertEqual(math.sin(math.pi / 2.0), calc_obj.calc(['pi', 2.0, '/', 'sin']))

    def test14(self):
        self.assertEqual(math.log10(100.0), calc_obj.calc([100.0, 'log10']))

    def test15(self):
        self.assertEqual(math.sin(math.pi / 2.0) * 111 * 6,
                         calc_obj.calc(['pi', 2.0, '/', 'sin', 111.0, '*', 6.0, '*']))

    def test16(self):
        self.assertEqual(2.0 * math.sin(math.pi / 2.0), calc_obj.calc([2.0, 'pi', 2.0, '/', 'sin', '*']))

    def test17(self):
        self.assertEqual(abs(-5.0), calc_obj.calc([0.0, 5.0, '-', 'abs']))

    def test18(self):
        self.assertEqual(round(123.456789), calc_obj.calc([123.456789, 'round']))

    # Associative
    def test19(self):
        self.assertEqual(102.0 % 12.0 % 7.0, calc_obj.calc([102.0,  12.0, '%', 7.0, '%']))

    def test20(self):
        self.assertEqual(100.0 / 4.0 / 3.0, calc_obj.calc([100.0,  4.0, '/', 3.0, '/']))

    def test21(self):
        self.assertEqual(2.0 ** 3.0 ** 4.0, calc_obj.calc([2.0, 3.0, 4.0, '^', '^']))

    # Comparison operators
    def test22(self):
        self.assertEqual(1.0 + 2.0 * 3.0 == 1.0 + 2.0 * 3.0,
                         calc_obj.calc([1.0, 2.0, 3.0, '*', '+', 1.0, 2.0, 3.0, '*', '+', '==']))

    def test23(self):
        self.assertEqual(math.e ** 5.0 >= math.e ** 5.0 + 1.0,
                         calc_obj.calc(['e', 5.0, '^', 'e', 5.0, '^', 1.0, '+', '>=']))

    def test24(self):
        self.assertEqual(1.0 + 2.0 * 4.0 / 3.0 + 1.0 != 1.0 + 2.0 * 4.0 / 3.0 + 2.0,
                         calc_obj.calc([1.0, 2.0, 4.0, '*', 3.0, '/', '+', 1.0, '+', 1.0, 2.0, 4.0, '*', 3.0, '/', '+',
                                        2.0, '+', '!=']))

    # Common tests
    def test25(self):
        self.assertEqual((100.0), calc_obj.calc([100.0]))

    def test26(self):
        self.assertEqual(666.0, calc_obj.calc([666.0]))

    def test27(self):
        self.assertEqual(-.1, calc_obj.calc([0.0, 0.1, '-']))

    def test28(self):
        self.assertEqual(1.0 / 3.0, calc_obj.calc([1.0, 3.0, '/']))

    def test29(self):
        self.assertEqual(1.0 / 3.0, calc_obj.calc([1.0, 3.0, '/']))

    def test30(self):
        self.assertEqual(.1*2.0**56.0, calc_obj.calc([0.1, 2.0, 56.0, '^',  '*']))

    def test31(self):
        self.assertEqual(math.e ** 34.0, calc_obj.calc(['e', 34.0, '^']))

    def test32(self):
        self.assertEqual((2.0 ** (math.pi/math.pi+math.e/math.e+2.0**0.0)),
                         calc_obj.calc([2.0, 'pi', 'pi', '/', 'e', 'e', '/', '+', 2.0, 0.0, '^', '+', '^']))

    def test33(self):
        self.assertEqual((2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))**(1.0/3.0), calc_obj.calc(
                        [2.0, 'pi', 'pi', '/', 'e', 'e', '/', '+', 2.0, 0.0, '^', '+', '^', 1.0, 3.0, '/', '^']))

    def test34(self):
        self.assertEqual(math.sin(math.pi/2.0**1.0) + math.log(1*4+2**2+1, 3**2),
                         calc_obj.calc(['pi', 2.0, 1.0, '^', '/', 'sin', 1.0, 4.0, '*', 2.0, 2.0, '^',
                                        '+', 1.0, '+',  3.0, 2.0, '^', 'log', '+']))

    def test35(self):
        self.assertEqual(10.0*math.e**0.0*math.log10(.4 -5.0/ -0.1-10.0) - -abs(-53.0/10.0) + -5.0,
                         calc_obj.calc([10.0, 'e', 0.0, '^', '*', 0.4, 5.0, 0.0, 0.1, '-', '/', '-', 10.0,
                                        '-', 'log10', '*', 0.0, 53.0, 10.0, '/', '-', 'abs', '+', 5.0, '-']))

    def test36(self):
        self.assertEqual(math.sin(-math.cos(-math.sin(3.0)-math.cos(-math.sin(-3.0*5.0)-math.sin(math.cos
                        (math.log10(43.0))))+math.cos(math.sin(math.sin(34.0-2.0**2.0))))--math.cos(1.0)--
                        math.cos(0.0)**3.0),
                         calc_obj.calc([0.0, 0.0, 3.0, 'sin', '-', 0.0, 0.0, 3.0, 5.0, '*', '-', 'sin', '-', 43.0,
                                        'log10', 'cos', 'sin', '-', 'cos', '-', 34.0, 2.0, 2.0, '^', '-', 'sin', 'sin',
                                        'cos', '+', 'cos', '-', 1.0, 'cos', '+', 0.0, 3.0, '^', 'cos', '+', 'sin']))

    def test37(self):
        self.assertEqual(2.0**(2.0**2.0*2.0**2.0), calc_obj.calc([2.0, 2.0, 2.0, '^', 2.0, 2.0, '^', '*', '^']))

    def test38(self):
        self.assertEqual(math.sin(math.e**math.log(math.e**math.e**math.sin(23.0), 45.0) +
                                  math.cos(3.0+math.log10(math.e**-math.e))),
                         calc_obj.calc(['e', 'e', 'e', 23.0, 'sin', '^', '^',  45.0, 'log', '^', 3.0, 'e', 0.0,
                                        'e', '-', '^', 'log10', '+', 'cos', '+', 'sin']))

    # Self-made cases
    def test52(self):
        self.assertEqual(100.0/3.0, calc_obj.calc([100.0, 3.0, '/']))

    def test54(self):
        self.assertEqual(100.0+3.0, calc_obj.calc([100.0, 3.0, '+']))

    def test55(self):
        self.assertEqual(100.0//3.0, calc_obj.calc([100.0, 3.0, '//']))

    def test56(self):
        self.assertEqual(math.sin(math.sin(1.0)), calc_obj.calc([1.0, 'sin', 'sin']))

    def test57(self):
        self.assertEqual(math.sin(math.sin(1.0))+1.0+math.sin(1.0),
                         calc_obj.calc([1.0, 'sin', 'sin', 1.0, '+', 1.0, 'sin', '+']))

    def test58(self):
        self.assertEqual(abs(-3.0), calc_obj.calc([0.0, 3.0, '-', 'abs']))

    def test59(self):
        self.assertEqual(round(3.56393), calc_obj.calc([3.56393, 'round']))

    def test60(self):
        self.assertEqual(abs(-round(3.56393)), calc_obj.calc([0.0, 3.56393, 'round', '-', 'abs']))

    # logarithms
    def test61(self):
        self.assertEqual(math.log(8.0, 2.0), calc_obj.calc([8.0, 2.0, 'log']))

    def test62(self):
        self.assertEqual(math.log(2.7), calc_obj.calc([2.7, 'log']))

    def test63(self):
        self.assertEqual((math.log(8.0, 2.0)-1.0)-2.0, calc_obj.calc([8.0, 2.0, 'log', 1.0, '-', 2.0, '-']))

    def test64(self):
        self.assertEqual(-math.log(8.0, 2.0), calc_obj.calc([0.0, 8.0, 2.0, 'log', '-']))

    def test65(self):
        self.assertEqual(math.log(8.0, 2.0)-1.0, calc_obj.calc([8.0, 2.0, 'log', 1.0, '-']))

    def test66(self):
        self.assertEqual(math.log(8.0, 2.0)*math.log(16.0, 2.0),
                         calc_obj.calc([8.0, 2.0, 'log', 16.0, 2.0, 'log', '*']))

    def test67(self):
        self.assertEqual(math.sin(math.log(8.0, 2.0)*math.log(16.0, 2.0)),
                         calc_obj.calc([8.0, 2.0, 'log', 16.0, 2.0, 'log', '*', 'sin']))

    def test68(self):
        self.assertEqual(math.log(8.0+20.0-1.0, 2.0+1.0),
                         calc_obj.calc([8.0, 20.0, '+', 1.0, '-', 2.0,  1.0, '+', 'log']))

    def test69(self):
        self.assertEqual(math.log10(100.0), calc_obj.calc([100.0, 'log10']))

    def test70(self):
        self.assertEqual(math.log(100.0, 10.0), calc_obj.calc([100.0, 10.0, 'log']))

    def test71(self):
        self.assertEqual((math.log10(100.0)-1.0)-2.0, calc_obj.calc([100.0, 'log10', 1.0, '-', 2.0, '-']))

    def test72(self):
        self.assertEqual(-math.log10(100.0), calc_obj.calc([0.0, 100.0, 'log10', '-']))

    def test73(self):
        self.assertEqual(math.log10(100.0)-1.0, calc_obj.calc([100.0, 'log10', 1.0, '-']))

    def test74(self):
        self.assertEqual(math.log10(100.0)*math.log10(1000.0), calc_obj.calc([100.0, 'log10', 1000.0, 'log10', '*']))

    def test75(self):
        self.assertEqual(math.sin(math.log10(100.0)*math.log10(1000.0)),
                         calc_obj.calc([100.0, 'log10', 1000.0, 'log10', '*', 'sin']))

    def test76(self):
        self.assertEqual(math.log10(800.0/2.0/4.0), calc_obj.calc([800.0, 2.0, '/', 4.0, '/', 'log10']))

    # pow
    def test77(self):
        self.assertEqual(math.pow(2.0, 4.0), calc_obj.calc([2.0, 4.0, 'pow']))

    def test78(self):
        self.assertEqual(math.log(math.pow(10.0, 2.0), 10), calc_obj.calc([10.0, 2.0, 'pow', 10.0, 'log']))

    def test79(self):
        self.assertEqual((math.pow(2.0, 4.0)-1.0)-2.0, calc_obj.calc([2.0, 4.0, 'pow', 1.0, '-', 2.0, '-']))

    def test80(self):
        self.assertEqual(-math.pow(2.0, 4.0), calc_obj.calc([0.0, 2.0, 4.0, 'pow', '-']))

    def test81(self):
        self.assertEqual(math.pow(2.0, 4.0)-1.0, calc_obj.calc([2.0, 4.0, 'pow', 1.0, '-']))

    def test82(self):
        self.assertEqual(math.pow(2.0, 4.0)*math.pow(2.0, 3.0), calc_obj.calc([2.0, 4.0, 'pow', 2.0, 3.0, 'pow', '*']))

    def test83(self):
        self.assertEqual(math.sin(math.pow(2.0, 4.0)*math.pow(2.0, 3.0)),
                         calc_obj.calc([2.0, 4.0, 'pow', 2.0, 3.0, 'pow', '*', 'sin']))

    def test84(self):
        self.assertEqual(math.pow(2.0**(2.0**2.0*2.0**2.0), math.log10(100.0)*math.log10(1000.0)),
                         calc_obj.calc([2.0, 2.0, 2.0, '^', 2.0, 2.0, '^', '*', '^',
                                        100.0, 'log10', 1000.0, 'log10', '*', 'pow']))

    def test85(self):
        self.assertEqual(13.0, calc_obj.calc([13.0]))

    def test86(self):
        self.assertEqual(-(-13.0), calc_obj.calc([0.0, 0.0, 13.0, '-', '-']))

    def test87(self):
        self.assertEqual(-(13.0), calc_obj.calc([0.0, 13.0, '-']))

    def test88(self):
        self.assertEqual(1.0*-13.0, calc_obj.calc([1.0, 0.0, 13.0, '-', '*']))

    def test89(self):
        self.assertEqual(1.0*(-13.0), calc_obj.calc([1.0, 0.0, 13.0, '-', '*']))

    def test90(self):
        self.assertEqual(1.0*(13.0), calc_obj.calc([1.0, 13.0, '*']))

    def test91(self):
        self.assertEqual((1.0+13.0), calc_obj.calc([1.0, 13.0, '+']))

    def test92(self):
        self.assertEqual(-1.0-(-1.0), calc_obj.calc([0.0, 1.0, '-', 0.0, 1.0, '-', '-']))

    def test93(self):
        self.assertEqual(((1.0)), calc_obj.calc([1.0]))

    def test94(self):
        self.assertEqual(-(-(-1.0)), calc_obj.calc([0.0, 0.0, 0.0, 1.0, '-', '-', '-']))


class TestCalcNegativeCases(unittest.TestCase):
    def test1(self):
        self.assertRaises(ValueError, lambda: calc_obj.calc([1.0, 2.0, 'sin']))

    def test2(self):
        self.assertRaises(ValueError, lambda: calc_obj.calc([1.0, 2.0, 3.0, 'sin']))

    def test3(self):
        self.assertRaises(ValueError, lambda: calc_obj.calc([1.0, 'pow']))

    def test4(self):
        self.assertRaises(ValueError, lambda: calc_obj.calc([1.0, 2.0, 3.0, 'pow']))


if __name__ == '__main__':
    unittest.main()
