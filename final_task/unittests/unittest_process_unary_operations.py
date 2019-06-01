import unittest

from final_task.pycalc_proc import PyCalcProcessing

calc_obj = PyCalcProcessing('1')


class TestProcessUnaryOperations(unittest.TestCase):
    def test1(self):
        list_ = calc_obj.process_unary_operations(['-', 13.0, ])
        self.assertEqual(list_, ['-', 13.0])

    def test2(self):
        list_ = calc_obj.process_unary_operations(['+', 13.0, ])
        self.assertEqual(list_, [13.0])

    def test3(self):
        list_ = calc_obj.process_unary_operations(['-', '-', 13.0, ])
        self.assertEqual(list_, [13.0])

    def test4(self):
        list_ = calc_obj.process_unary_operations(['-', '-', '-', 13.0, ])
        self.assertEqual(list_, ['-', 13.0])

    def test5(self):
        list_ = calc_obj.process_unary_operations(['-', '-', '-', '-', 13.0, ])
        self.assertEqual(list_, [13.0])

    def test6(self):
        list_ = calc_obj.process_unary_operations(['+', '-', '+', '+', 13.0, ])
        self.assertEqual(list_, ['-', 13.0])

    def test7(self):
        list_ = calc_obj.process_unary_operations(['-', '(', '-', 13.0, ')'])
        self.assertEqual(list_, ['-', '(', '-', 13.0, ')'])

    def test8(self):
        list_ = calc_obj.process_unary_operations(['-', '(', '-', '-', 13.0, ')'])
        self.assertEqual(list_, ['-', '(', 13.0, ')'])

    def test9(self):
        list_ = calc_obj.process_unary_operations(['+', '+', '+', '+', 13.0, ])
        self.assertEqual(list_, [13.0])

    def test10(self):
        list_ = calc_obj.process_unary_operations([1.0, '*', '-', '-', 13.0, ])
        self.assertEqual(list_, [1.0, '*', 13.0])

    def test11(self):
        list_ = calc_obj.process_unary_operations([1.0, '*', '-', 13.0, ])
        self.assertEqual(list_, [1.0, '*', '-', 13.0])

    def test12(self):
        list_ = calc_obj.process_unary_operations([1.0, '*', '+', 13.0, ])
        self.assertEqual(list_, [1.0, '*', 13.0])

    def test13(self):
        list_ = calc_obj.process_unary_operations([1.0, '*', '(', '+', 13.0, ')'])
        self.assertEqual(list_, [1.0, '*', '(', 13.0, ')'])

    def test14(self):
        list_ = calc_obj.process_unary_operations(['(', 1.0, '+', 13.0, ')'])
        self.assertEqual(list_, ['(', 1.0, '+', 13.0, ')'])

    def test15(self):
        list_ = calc_obj.process_unary_operations(['-', '-', '-', '-', '-', 1.0, '-', '+', '(', '-', 1.0, ')'])
        self.assertEqual(list_, ['-', 1.0, '-', '(', '-', 1.0, ')'])

    def test16(self):
        list_ = calc_obj.process_unary_operations(['-', '+', '-', '-', '-', '+', '-', 1.0])
        self.assertEqual(list_, ['-', 1.0])

    def test17(self):
        list_ = calc_obj.process_unary_operations(['-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-', 1.0])
        self.assertEqual(list_, [1.0])

    def test18(self):
        list_ = calc_obj.process_unary_operations(['-', '+', '(', '-', '-', '+', '-', 1.0, ')'])
        self.assertEqual(list_, ['-', '(', '-', 1.0, ')'])

    def test19(self):
        list_ = calc_obj.process_unary_operations(['+', '+', '-', '-', '+', '+', '-', '(', '-', 1.0, ')'])
        self.assertEqual(list_, ['-', '(', '-', 1.0, ')'])

    def test20(self):
        list_ = calc_obj.process_unary_operations([1, '-', '-', '-', 1.0])
        self.assertEqual(list_, [1.0, '-', 1.0])

    def test21(self):
        list_ = calc_obj.process_unary_operations([1.0, '-', '-', 1.0, '-', '-', 1.0])
        self.assertEqual(list_, [1.0, '+', 1.0, '+', 1.0])

    def test22(self):
        list_ = calc_obj.process_unary_operations([1.0, '-', '+', 1.0, '+', '-', 1.0])
        self.assertEqual(list_, [1.0, '-', 1.0, '-', 1.0])

    def test23(self):
        list_ = calc_obj.process_unary_operations(['+', '+', '+', '+', '+', 1.0])
        self.assertEqual(list_, [1.0])

    def test24(self):
        list_ = calc_obj.process_unary_operations(['-', '-', '-', '-', '-', 1.0])
        self.assertEqual(list_, ['-', 1.0])

    def test25(self):
        list_ = calc_obj.process_unary_operations(['+', '+', '(', '+', '(', '+', '+', 1.0, ')', ')'])
        self.assertEqual(list_, ['(', '(', 1.0, ')', ')'])

    def test26(self):
        list_ = calc_obj.process_unary_operations(['-', '(', '-', '+', '(', '-', '+', 1.0, ')', ')'])
        self.assertEqual(list_, ['-', '(', '-', '(', '-', 1.0, ')', ')'])

    def test27(self):
        list_ = calc_obj.process_unary_operations(['+', 1.0, ])
        self.assertEqual(list_, [1.0])

    def test28(self):
        list_ = calc_obj.process_unary_operations([6.0, '-', '(', '-', 13.0, ')'])
        self.assertEqual(list_, [6.0, '-', '(', '-', 13.0, ')'])

    def test29(self):
        list_ = calc_obj.process_unary_operations([1.0, '-', '-', '-', 1.0])
        self.assertEqual(list_, [1.0, '-', 1.0])

    def test30(self):
        list_ = calc_obj.process_unary_operations(['-', '+', '-', '-', '-', '+', '-', 1.0])
        self.assertEqual(list_, ['-', 1.0])

    def test31(self):
        list_ = calc_obj.process_unary_operations(
            ['sin', '(', '-', 'cos', '(', '-', 'sin', '(', 3.0, ')', '-', 'cos', '(', '-',
             'sin', '(', '-', 3.0, '*', 5.0, ')', '-', 'sin', '(', 'cos', '(', 'log10',
             '(', 43.0, ')', ')', ')', ')', '+', 'cos', '(', 'sin', '(', 'sin', '(', 34.0,
             '-', 2.0, '^', 2.0, ')', ')', ')', ')', '-', '-', 'cos', '(', 1.0, ')', '-',
             '-', 'cos', '(', 0.0, ')', '^', 3.0, ')'])
        self.assertEqual(list_, ['sin', '(', '-', 'cos', '(', '-', 'sin', '(', 3.0, ')', '-', 'cos', '(', '-', 'sin',
                                 '(', '-', 3.0, '*', 5.0, ')', '-', 'sin', '(', 'cos', '(', 'log10', '(', 43.0, ')',
                                 ')', ')', ')', '+', 'cos', '(', 'sin', '(', 'sin', '(', 34.0, '-', 2.0, '^', 2.0, ')',
                                 ')', ')', ')', '+', 'cos', '(', 1.0, ')', '+', 'cos', '(', 0.0, ')', '^', 3.0, ')'])

    def test32(self):
        list_ = calc_obj.process_unary_operations(
            [10.0, '*', 'e', '^', 0.0, '*', 'log10', '(', 0.4, '-', 5.0, '/', '-', 0.1,
             '-', 10.0, ')', '-', '-', 'abs', '(', '-', 53.0, '/', 10.0, ')', '+', '-',
             5.0])
        self.assertEqual(list_, [10.0, '*', 'e', '^', 0.0, '*', 'log10', '(', 0.4, '-', 5.0, '/', '-', 0.1, '-',
                                 10.0, ')', '+', 'abs', '(', '-', 53.0, '/', 10.0, ')', '-', 5.0])


if __name__ == '__main__':
    unittest.main()
