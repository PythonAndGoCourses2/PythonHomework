import unittest

from final_task.pycalc_proc import PyCalcProcessing

calc_obj = PyCalcProcessing('1')


class ExpectedFailureTestCase(unittest.TestCase):
    # Error cases
    def test1(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['+', '+']))

    def test2(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['+']))

    def test3(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([1.0, '-']))

    def test4(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['ee']))

    def test5(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['==', 7.0]))

    def test6(self):
        self.assertRaises(ValueError,
                          lambda: calc_obj.validate_parsed_list([1.0, '+', 2.0, '(', 3.0, '*', 4.0, ')', ')']))

    def test7(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '(', 1.0, '+', 2.0, ')']))

    def test8(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', ')']))

    def test9(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['log10', 0.0, '(', 100.0, ')']))

    def test10(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['-', '-', '-', '-', '-', '-']))

    def test11(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', ')']))

    def test12(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([6.0, '*', '*', 6.0]))

    def test13(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', ')']))

    def test14(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '(', '(', '(', '(', ]))

    def test15(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([77.0, '==', '==', 77.0]))

    def test16(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['_', '+', 'son']))

    def test17(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-', 4.0, ')', '+', 2.0]))

    def test18(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', ',', 77.0, '-', 4.0, ')', '+', 2.0]))

    def test19(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '//', 77.0, '-', 4.0, ')', '+', 2.0]))

    def test20(self):
        self.assertRaises(ValueError,
                          lambda: calc_obj.validate_parsed_list(['(', 1.0, '+', 5.0, ')', '(', 1.0, '+', 5.0, ')']))

    def test21(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-', 4.0, ')', '.', 2.0]))

    def test22(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', ',', 77.0, '-', 4.0, ')', ',', 2.0]))

    def test23(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '//', 77.0, '-', 4.0, ')',
                                                                             'sin', '(', 2.0, ')']))

    def test24(self):
        self.assertRaises(ValueError,
                          lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-', 4.0, ')', 2.0, '+', 1.0]))

    def test25(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', ',', 77.0, '-', 4.0, ')', 'e']))

    def test26(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '//', 77.0, '-', 4.0,
                                                                             ')', 'sin', '(', 2.0, ')']))

    def test27(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-', 4.0, ')',
                                                                             '.', '(', 2.0, '+', '1']))

    def test28(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-',

                                                                             4.0, '.', '.', ')']))

    def test29(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-', 4.0, ')',
                                                                             '.', '(', 2.0, '+', '1']))

    def test30(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-', 4.0, ')',
                                                                             '.', ',', 2.0, '+', '1']))

    def test31(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-', 4.0, ')',
                                                                             '.', '-', 2.0, '+', '1']))

    def test32(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-', 4.0, ')',
                                                                             '.', 'sin', '(', 2.0, ')']))

    def test33(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['(', '.', 77.0, '-', 4.0, ')', '.', 'e']))

    def test34(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['-', ')', 4.0]))

    def test35(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['-', '.', 4.0]))

    def test36(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['-', ',', 4.0]))

    def test37(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['-', '//', 4.0]))

    def test38(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([26.0, '//', ')', 4.0]))

    def test39(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([26.0, '//', '.', 4.0]))

    def test40(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([26.0, '//', ',', 4.0]))

    def test41(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([26.0, '//', '%', 4.0]))

    def test42(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['cos', ')', 4.0, ')']))

    def test43(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['cos', '.', 4.0, ')']))

    def test44(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['cos', ',', 4.0, ')']))

    def test45(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['cos', '-', 4.0, ')']))

    def test46(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['cos', '//', 4.0, ')']))

    def test47(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['cos', 'cos', 4.0, ')']))

    def test48(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['cos', 4.0, ')']))

    def test49(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['cos', 'e', 4.0, ')']))

    def test50(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([4.0, '(', '+', 5.0, ')']))

    def test51(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([4.0, '.', '+', 5.0]))

    def test52(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([4.0, 'sin', '(', 5.0, ')']))

    def test53(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([4.0, 3.0, '+', 5.0]))

    def test54(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([4.0, 'e', '+', 5.0, ')']))

    def test55(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['e', '(', '+', 'pi']))

    def test56(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['e', '.', '+', 'pi']))

    def test57(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['e', 'sin', '(', 3.0, ')']))

    def test58(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list(['e', 3.0, '+', 'pi']))

    # matched parentheses
    def test59(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([15.0, '*', '(', 25.0, '+', 1.0]))

    def test60(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([15.0, '*', 25.0, '+', 1.0, ')']))

    def test61(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([15.0, '*', ')', 25.0, '+', 1.0, ')']))

    def test62(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([15.0, '*', 25.0, '+', 1.0, '(', ')']))

    def test63(self):
        self.assertRaises(ValueError, lambda: calc_obj.validate_parsed_list([15.0, '*', 25.0, '+', '(', 1.0,
                                                                             '+', ')', 1.0, ')']))


class ExpectedSuccessTestCase(unittest.TestCase):
    def test1(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(['-', 13.0]))

    def test2(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([6.0, '-', '(', '-',
                                                        13.0, ')']))

    def test3(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([1.0, '-', '-', '-',
                                                        1.0]))

    def test4(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list(['-', '+', '-', '-',
                                                        '-', '+', '-', 1.0]))

    def test5(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list([1.0, '+', 2.0,
                                                                                                         '*', 2.0]))

    def test6(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([1.0, '+', '(', 2.0, '+',
                                                        3.0, '*', 2.0, ')', '*',
                                                        3.0]))

    def test7(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([10.0, '*', '(', 2.0,
                                                        '+', 1.0, ')']))

    def test8(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([10.0, '^', '(', 2.0,
                                                        '+', 1.0, ')']))

    def test9(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([100.0, '/', 3.0,
                                                        '^', 2.0]))

    def test10(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([100.0, '/', 3.0, '%',
                                                        2.0, '^', 2.0]))

    def test11(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list(['pi', '+', 'e']))

    def test12(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list(['log', '(', 'e', ')']))

    def test13(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list(['sin', '(', 'pi', '/',
                                                        2.0, ')']))

    def test14(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(['log10', '(',
                                                                                                         100.0, ')']))

    def test15(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(
            ['sin', '(', 'pi', '/', 2.0, ')', '*', 111.0, '*', 6.0]))

    def test16(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(
            [2.0, '*', 'sin', '(', 'pi', '/', 2.0, ')']))

    def test17(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list(['abs', '(', '-', 5.0,
                                                        ')']))

    def test18(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(['round', '(',
                                                                                                         123.456789,
                                                                                                         ')']))

    def test19(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([102.0, '%', 12.0,
                                                        '%', 7.0]))

    def test20(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([100.0, '/', 4.0, '/',
                                                        3.0]))

    def test21(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([2.0, '^', 3.0, '^',
                                                        4.0]))

    def test22(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(
            [1.0, '+', 2.0, '*', 3.0, '==', 1.0, '+', 2.0, '*', 3.0]))

    def test23(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(
            ['e', '^', 5.0, '>=', 'e', '^', 5.0, '+', 1.0]))

    def test24(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(
            [1.0, '+', 2.0, '*', 4.0, '/', 3.0, '+', 1.0, '!=', 1.0, '+', 2.0, '*', 4.0, '/', 3.0, '+', 2.0]))

    def test25(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list(['(', 100.0, ')']))

    def test26(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list([666.0]))

    def test27(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(['-', 0.1]))

    def test28(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([1.0, '/', 3.0]))

    def test29(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([0.1, '*', 2.0, '^',
                                                        56.0]))

    def test30(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list(['e', '^', 34.0]))

    def test31(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list(['(', 2.0, '^', '(', 'pi', '/', 'pi', '+', 'e',
                                                        '/', 'e', '+', 2.0, '^', 0.0, ')', ')']))

    def test32(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list(['(', 2.0, '^', '(', 'pi', '/', 'pi', '+', 'e',
                                                        '/', 'e', '+', 2.0, '^', 0.0, ')', ')',
                                                        '^', '(', 1.0, '/', 3.0, ')']))

    def test33(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(
            [10.0, '*', 'e', '^', 0.0, '*', 'log10', '(', 0.4, '-', 5.0, '/', '-', 0.1, '-',
             10.0, ')', '-', '-', 'abs', '(', '-', 53.0, '/', 10.0, ')', '+', '-', 5.0]))

    def test34(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(
            ['sin', '(', '-', 'cos', '(', '-', 'sin', '(', 3.0, ')', '-', 'cos',
             '(', '-', 'sin', '(', '-', 3.0, '*', 5.0, ')', '-', 'sin', '(', 'cos', '(',
             'log10', '(', 43.0, ')', ')', ')', ')', '+', 'cos', '(', 'sin', '(', 'sin', '(',
             34.0, '-', 2.0, '^', 2.0, ')', ')', ')', ')', '-', '-', 'cos', '(', 1.0, ')', '-', '-',
             'cos', '(', 0.0, ')', '^', 3.0, ')']))

    def test35(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(
            [2.0, '^', '(', 2.0, '^', 2.0, '*', 2.0, '^', 2.0, ')']))

    def test36(self):
        self.assertEqual('Formula was validated! Errors were not found.', calc_obj.validate_parsed_list(
            ['sin', '(', 'e', '^', 'log', '(', 'e', '^', 'e', '^', 'sin', '(', 23.0, ')', ',', 45.0,
             ')', '+', 'cos', '(', 3.0, '+', 'log10', '(', 'e', '^', '-', 'e', ')', ')', ')']))

    def test37(self):
        self.assertEqual('Formula was validated! Errors were not found.',
                         calc_obj.validate_parsed_list([1.0, '*', '-', 13.0]))

    def test38(self):
        self.assertEqual('Formula was validated! '
                         'Errors were not found.',
                         calc_obj.validate_parsed_list(['log', '(', 1.0, ',', '-', 13.0, ')']))

    def test39(self):
        self.assertEqual('Formula was validated! '
                         'Errors were not found.', calc_obj.validate_parsed_list(['log', '(', 1.0, ',',
                                                                                  '(', '-', 13.0, ')', ')']))

    # incorrect number of arguments processing in calc
    def test40(self):
        self.assertEqual('Formula was validated! '
                         'Errors were not found.', calc_obj.validate_parsed_list(['pow', '(', 1.0, ')']))


if __name__ == '__main__':
    unittest.main()
