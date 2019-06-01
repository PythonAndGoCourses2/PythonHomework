import unittest

from py_calc import PyCalcProcessing

calc_obj = PyCalcProcessing('1')


class TestSorting(unittest.TestCase):

    # Unary operators
    def test1(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', 13.0]):
            list_.append(el)
        self.assertEqual(list_, [0.0, 13.0, '-'])

    def test2(self):
        list_ = []
        for el in calc_obj.sort_to_polish([6.0, '-', '(', '-', 13.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [6.0, 0.0, 13.0, '-', '-'])

    def test3(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '-', 1.0]):
            list_.append(el)
        self.assertEqual(list_, [1.0, 1.0, '-'])

    def test4(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', 1.0]):
            list_.append(el)
        self.assertEqual(list_, [0.0, 1.0, '-'])

    # Operation priority
    def test5(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '+', 2.0, '*', 2.0]):
            list_.append(el)
        self.assertEqual(list_, [1.0, 2.0, 2.0, '*', '+'])

    def test6(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '+', '(', 2.0, '+', 3.0, '*', 2.0, ')', '*', 3.0]):
            list_.append(el)
        self.assertEqual(list_, [1.0, 2.0, 3.0, 2.0, '*', '+', 3.0, '*', '+'])

    def test7(self):
        list_ = []
        for el in calc_obj.sort_to_polish([10.0, '*', '(', 2.0, '+', 1.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [10.0, 2.0, 1.0, '+', '*'])

    def test8(self):
        list_ = []
        for el in calc_obj.sort_to_polish([10.0, '^', '(', 2.0, '+', 1.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [10.0, 2.0, 1.0, '+', '^'])

    def test9(self):
        list_ = []
        for el in calc_obj.sort_to_polish([100.0, '/', 3.0, '^', 2.0]):
            list_.append(el)
        self.assertEqual(list_, [100.0, 3.0, 2.0, '^', '/'])

    def test10(self):
        list_ = []
        for el in calc_obj.sort_to_polish([100.0, '/', 3.0, '%', 2.0, '^', 2.0]):
            list_.append(el)
        self.assertEqual(list_, [100.0, 3.0, '/', 2.0, 2.0, '^', '%'])

    # Functions and constants
    def test11(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['pi', '+', 'e']):
            list_.append(el)
        self.assertEqual(list_, ['pi', 'e', '+'])

    def test12(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log', '(', 'e', ')']):
            list_.append(el)
        self.assertEqual(list_, ['e', 'log'])

    def test13(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['sin', '(', 'pi', '/', 2.0, ')']):
            list_.append(el)
        self.assertEqual(list_, ['pi', 2.0, '/', 'sin'])

    def test14(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log10', '(', 100.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [100.0, 'log10'])

    def test15(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['sin', '(', 'pi', '/', 2.0, ')', '*', 111.0, '*', 6.0]):
            list_.append(el)
        self.assertEqual(list_, ['pi', 2.0, '/', 'sin', 111.0, '*', 6.0, '*'])

    def test16(self):
        list_ = []
        for el in calc_obj.sort_to_polish([2.0, '*', 'sin', '(', 'pi', '/', 2.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [2.0, 'pi', 2.0, '/', 'sin', '*'])

    def test17(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['abs', '(', '-', 5.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 5.0, '-', 'abs'])

    def test18(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['round', '(', 123.456789, ')']):
            list_.append(el)
        self.assertEqual(list_, [123.456789, 'round'])

    # Associative
    def test19(self):
        list_ = []
        for el in calc_obj.sort_to_polish([102.0, '%', 12.0, '%', 7.0]):
            list_.append(el)
        self.assertEqual(list_, [102.0,  12.0, '%', 7.0, '%'])

    def test20(self):
        list_ = []
        for el in calc_obj.sort_to_polish([100.0, '/', 4.0, '/', 3.0]):
            list_.append(el)
        self.assertEqual(list_, [100.0,  4.0, '/', 3.0, '/'])

    def test21(self):
        list_ = []
        for el in calc_obj.sort_to_polish([2.0, '^', 3.0, '^', 4.0]):
            list_.append(el)
        self.assertEqual(list_, [2.0, 3.0, 4.0, '^', '^'])

    # Comparison operators
    def test22(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '+', 2.0, '*', 3.0, '==', 1.0, '+', 2.0, '*', 3.0]):
            list_.append(el)
        self.assertEqual(list_, [1.0, 2.0, 3.0, '*', '+', 1.0, 2.0, 3.0, '*', '+', '=='])

    def test23(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['e', '^', 5.0, '>=', 'e', '^', 5.0, '+', 1.0]):
            list_.append(el)
        self.assertEqual(list_, ['e', 5.0, '^', 'e', 5.0, '^', 1.0, '+', '>='])

    def test24(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '+', 2.0, '*', 4.0, '/', 3.0, '+', 1.0, '!=',
                                  1.0, '+', 2.0, '*', 4.0, '/', 3.0, '+', 2.0]):
            list_.append(el)
        self.assertEqual(list_, [1.0, 2.0, 4.0, '*', 3.0, '/', '+', 1.0, '+', 1.0,
                                 2.0, 4.0, '*', 3.0, '/', '+', 2.0, '+', '!='])

    # Common tests
    def test25(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['(', 100.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [100.0])

    def test26(self):
        list_ = []
        for el in calc_obj.sort_to_polish([666.0]):
            list_.append(el)
        self.assertEqual(list_, [666.0])

    def test27(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', 0.1]):
            list_.append(el)
        self.assertEqual(list_, [0.0, 0.1, '-'])

    def test28(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '/', 3.0]):
            list_.append(el)
        self.assertEqual(list_, [1.0, 3.0, '/'])

    def test29(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '/', 3.0]):
            list_.append(el)
        self.assertEqual(list_, [1.0, 3.0, '/'])

    def test30(self):
        list_ = []
        for el in calc_obj.sort_to_polish([0.1, '*', 2.0, '^', 56.0]):
            list_.append(el)
        self.assertEqual(list_, [0.1, 2.0, 56.0, '^',  '*'])

    def test31(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['e', '^', 34.0]):
            list_.append(el)
        self.assertEqual(list_, ['e', 34.0, '^'])

    def test32(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['(', 2.0, '^', '(', 'pi', '/', 'pi', '+', 'e', '/', 'e',
                                  '+', 2.0, '^', 0.0, ')', ')']):
            list_.append(el)
        self.assertEqual(list_, [2.0, 'pi', 'pi', '/', 'e', 'e', '/', '+', 2.0, 0.0, '^', '+', '^'])

    def test33(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['(', 2.0, '^', '(', 'pi', '/', 'pi', '+', 'e', '/', 'e', '+', 2.0, '^', 0.0, ')',
                                  ')', '^', '(', 1.0, '/', 3.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [2.0, 'pi', 'pi', '/', 'e', 'e', '/', '+', 2.0, 0.0, '^', '+',
                                 '^', 1.0, 3.0, '/', '^'])

    # TODO: fixed
    def test34(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log', '(', 1.0, '*', 4.0, '+', 2.0, '^', 2.0, '+', 1.0, ',', 3.0, '^', 2.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [1.0, 4.0, '*', 2.0, 2.0, '^', '+', 1.0, '+', ',', 3.0, 2.0, '^', 'log'])

    # TODO: problem, when unary operations go after binary without parentheses as -5/ -0.1
    def test35(self):  # 10*e^0*log10(.4 -5/ -0.1-10)+abs(-53/10)-5
        list_ = []
        for el in calc_obj.sort_to_polish([10.0, '*', 'e', '^', 0.0, '*', 'log10', '(', 0.4, '-', 5.0, '/', '-', 0.1,
                                  '-', 10.0, ')', '+', 'abs', '(', '-', 53.0, '/', 10.0, ')', '-', 5.0]):
            list_.append(el)
        self.assertEqual(list_, [10.0, 'e', 0.0, '^', '*', 0.4, 5.0, 0.0, 0.1, '-', '/', '-', 10.0, '-', 'log10', '*',
                                 0.0, 53.0, 10.0, '/', '-', 'abs', '+', 5.0, '-'])

    def test36(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['sin', '(', '-', 'cos', '(', '-', 'sin', '(', 3.0, ')', '-', 'cos', '(', '-', 'sin',
                                  '(', '-', 3.0, '*', 5.0, ')', '-', 'sin', '(', 'cos', '(', 'log10', '(', 43.0, ')',
                                  ')', ')', ')', '+', 'cos', '(', 'sin', '(', 'sin', '(', 34.0, '-', 2.0, '^', 2.0, ')',
                                  ')', ')', ')', '+', 'cos', '(', 1.0, ')', '+', 'cos', '(', 0.0, ')', '^', 3.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 0.0, 3.0, 'sin', '-', 0.0, 0.0, 3.0, 5.0, '*', '-', 'sin', '-', 43.0, 'log10',
                                 'cos', 'sin', '-', 'cos', '-', 34.0, 2.0, 2.0, '^', '-', 'sin', 'sin', 'cos', '+',
                                 'cos', '-', 1.0, 'cos', '+', 0.0, 3.0, '^', 'cos', '+', 'sin'])

    def test37(self):
        list_ = []
        for el in calc_obj.sort_to_polish([2.0, '^', '(', 2.0, '^', 2.0, '*', 2.0, '^', 2.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [2.0, 2.0, 2.0, '^', 2.0, 2.0, '^', '*', '^'])

    # TODO: process log correctly (if we put here first argument of log in (), everything will be done correctly)
    # TODO: problem, when unary operations go after binary without parentheses as e^-e
    def test38(self):  # sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))
        list_ = []
        for el in calc_obj.sort_to_polish(['sin', '(', 'e', '^', 'log', '(', 'e', '^', 'e', '^', 'sin',
                                  '(', 23.0, ')', ',', 45.0, ')', '+', 'cos', '(', 3.0, '+', 'log10',
                                  '(', 'e', '^', '-', 'e', ')', ')', ')']):
            list_.append(el)
        self.assertEqual(list_, ['e', 'e', 'e', 23.0, 'sin', '^', '^', ',', 45.0, 'log', '^', 3.0, 'e', 0.0,
                                 'e', '-', '^', 'log10', '+', 'cos', '+', 'sin'])

    # Self-made cases
    def test52(self):
        list_ = []
        for el in calc_obj.sort_to_polish([100.0, '/', 3.0]):
            list_.append(el)
        self.assertEqual(list_, [100.0, 3.0, '/'])

    def test54(self):
        list_ = []
        for el in calc_obj.sort_to_polish([100.0, '+', 3.0]):
            list_.append(el)
        self.assertEqual(list_, [100.0, 3.0, '+'])

    def test55(self):
        list_ = []
        for el in calc_obj.sort_to_polish([100.0, '//', 3.0]):
            list_.append(el)
        self.assertEqual(list_, [100.0, 3.0, '//'])

    def test56(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['sin', '(', 'sin', '(', 1.0, ')', ')']):
            list_.append(el)
        self.assertEqual(list_, [1.0, 'sin', 'sin'])

    def test57(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['sin', '(', 'sin', '(', 1.0, ')', ')', '+', 1.0, '+', 'sin', '(', 1.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [1.0, 'sin', 'sin', 1.0, '+', 1.0, 'sin', '+'])

    def test58(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['abs', '(', '-', 3.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 3.0, '-', 'abs'])

    def test59(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['round', '(', 3.56393, ')']):
            list_.append(el)
        self.assertEqual(list_, [3.56393, 'round'])

    def test60(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['abs', '(', '-', 'round', '(', 3.56393, ')', ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 3.56393, 'round', '-', 'abs'])

    # logarithms
    def test61(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log', '(', 8.0, ',', 2.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [8.0, ',', 2.0, 'log'])

    def test62(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log', '(', 2.7, ')']):
            list_.append(el)
        self.assertEqual(list_, [2.7, 'log'])

    def test63(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['(', 'log', '(', 8.0, ',', 2.0, ')', '-', 1.0, ')', '-', 2.0]):
            list_.append(el)
        self.assertEqual(list_, [8.0, ',', 2.0, 'log', 1.0, '-', 2.0, '-'])

    def test64(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', 'log', '(', 8.0, ',', 2.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 8.0, ',', 2.0, 'log', '-'])

    def test65(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log', '(', 8.0, ',', 2.0, ')', '-', 1.0]):
            list_.append(el)
        self.assertEqual(list_, [8.0, ',', 2.0, 'log', 1.0, '-'])

    def test66(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log', '(', 8.0, ',', 2.0, ')', '*', 'log', '(', 16.0, ',', 2.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [8.0, ',', 2.0, 'log', 16.0, ',', 2.0, 'log', '*'])

    def test67(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['sin', '(', 'log', '(', 8.0, ',', 2.0, ')', '*',
                                  'log', '(', 16.0, ',', 2.0, ')', ')']):
            list_.append(el)
        self.assertEqual(list_, [8.0, ',', 2.0, 'log', 16.0, ',', 2.0, 'log', '*', 'sin'])

    # TODO: fixed
    def test68(self):  # log(8+20-1,2+1)
        list_ = []
        for el in calc_obj.sort_to_polish(['log', '(', 8.0, '+', 20.0, '-', 1.0, ',', 2.0, '+', 1.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [8.0, 20.0, '+', 1.0, '-', ',', 2.0,  1.0, '+', 'log'])

    def test69(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log10', '(', 100.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [100.0, 'log10'])

    def test70(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log', '(', 100.0, ',', 10.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [100.0, ',', 10.0, 'log'])

    def test71(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['(', 'log10', '(', 100.0, ')', '-', 1.0, ')', '-', 2.0]):
            list_.append(el)
        self.assertEqual(list_, [100.0, 'log10', 1.0, '-', 2.0, '-'])

    def test72(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', 'log10', '(', 100.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 100.0, 'log10', '-'])

    def test73(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log10', '(', 100.0, ')', '-', 1.0]):
            list_.append(el)
        self.assertEqual(list_, [100.0, 'log10', 1.0, '-'])

    def test74(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log10', '(', 100.0, ')', '*', 'log10', '(', 1000.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [100.0, 'log10', 1000.0, 'log10', '*'])

    def test75(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['sin', '(', 'log10', '(', 100.0, ')', '*', 'log10', '(', 1000.0, ')', ')']):
            list_.append(el)
        self.assertEqual(list_, [100.0, 'log10', 1000.0, 'log10', '*', 'sin'])

    def test76(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['log10', '(', 800.0, '/', 2.0, '/', 4.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [800.0, 2.0, '/', 4.0, '/', 'log10'])

    # pow
    def test77(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['pow', '(', 2.0, ',', 4.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [2.0, ',', 4.0, 'pow'])

    # TODO: process log correctly (if we put here first argument of log in (), everything will be done correctly)
    def test78(self):  # log(pow(10,2),10)
        list_ = []
        for el in calc_obj.sort_to_polish(['log', '(', 'pow', '(', 10.0, ',', 2.0, ')', ',', 10.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [10.0, ',', 2.0, 'pow', ',', 10.0, 'log'])

    def test79(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['(', 'pow', '(', 2.0, ',', 4.0, ')', '-', 1.0, ')', '-', 2.0]):
            list_.append(el)
        self.assertEqual(list_, [2.0, ',', 4.0, 'pow', 1.0, '-', 2.0, '-'])

    def test80(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', 'pow', '(', 2.0, ',', 4.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 2.0, ',', 4.0, 'pow', '-'])

    def test81(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['pow', '(', 2.0, ',', 4.0, ')', '-', 1.0]):
            list_.append(el)
        self.assertEqual(list_, [2.0, ',', 4.0, 'pow', 1.0, '-'])

    def test82(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['pow', '(', 2.0, ',', 4.0, ')', '*', 'pow', '(', 2.0, ',', 3.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [2.0, ',', 4.0, 'pow', 2.0, ',', 3.0, 'pow', '*'])

    def test83(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['sin', '(', 'pow', '(', 2.0, ',', 4.0, ')', '*', 'pow', '(', 2.0, ',', 3.0, ')', ')']):
            list_.append(el)
        self.assertEqual(list_, [2.0, ',', 4.0, 'pow', 2.0, ',', 3.0, 'pow', '*', 'sin'])

    # TODO: process pow correctly (if we put arguments of pow in (), everything will be done correctly)
    def test84(self):  # pow(2.0^(2.0^2.0*2.0^2.0),sin(log10(100)*log10(1000)))
        list_ = []
        for el in calc_obj.sort_to_polish(['pow', '(', 2.0, '^', '(', 2.0, '^', 2.0, '*', 2.0, '^', 2.0, ')', ',', 'sin', '(',
                                 'log10', '(', 100.0, ')', '*', 'log10', '(', 1000.0, ')', ')', ')']):
            list_.append(el)
        self.assertEqual(list_, [2.0, 2.0, 2.0, '^', 2.0, 2.0, '^', '*', '^', ',', 100.0, 'log10', 1000.0, 'log10', '*',
                                 'sin', 'pow'])

    # unary_operations
    def test85(self):
        list_ = []
        for el in calc_obj.sort_to_polish([13.0]):
            list_.append(el)
        self.assertEqual(list_, [13.0])

    def test86(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', '(', '-', 13.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 0.0, 13.0, '-', '-'])

    def test87(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', '(', 13.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 13.0, '-'])

    # TODO: problem, when unary operations go after binary without parentheses
    def test88(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '*', '-', 13.0]):
            list_.append(el)
        self.assertEqual(list_, [1.0, 0.0, 13.0, '-', '*'])

    def test89(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '*', '(', '-', 13.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [1.0, 0.0, 13.0, '-', '*'])

    def tes90(self):
        list_ = []
        for el in calc_obj.sort_to_polish([1.0, '*', '(', 13.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [1.0, 13.0, '*'])

    def test91(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['(', 1.0, '+', 13.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [1.0, 13.0, '+'])

    def test92(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', 1.0, '-', '(', '-', 1.0, ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 1.0, '-', 0.0, 1.0, '-', '-'])

    def test93(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['(', '(', 1.0, ')', ')']):
            list_.append(el)
        self.assertEqual(list_, [1.0])

    def test94(self):
        list_ = []
        for el in calc_obj.sort_to_polish(['-', '(', '-', '(', '-', 1.0, ')', ')']):
            list_.append(el)
        self.assertEqual(list_, [0.0, 0.0, 0.0, 1.0, '-', '-', '-'])


if __name__ == '__main__':
    unittest.main()
