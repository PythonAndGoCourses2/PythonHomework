"""

module which contains unit tests for calculating methods

"""
import logic
import constants
import unittest
import pycodestyle
import main_funcs

logic.import_usr_imports(constants.imports)

methods = main_funcs.calc_init(constants.imports)


class LogicTests(unittest.TestCase):

    def test_get_item_by_type(self):
        self.assertEqual(logic._get_item_by_type('2', methods), 2)
        self.assertEqual(logic._get_item_by_type('2.4', methods), 2.4)
        self.assertEqual(logic._get_item_by_type('True', methods), True)

    def test_str_parse(self):
        self.assertEqual(logic.str_parse('2+2', methods), ['2', '+', '2'])

    def test_priority(self):
        self.assertEqual(logic._get_priority('+'), 2)
        self.assertEqual(logic._get_priority('*'), 3)
        self.assertEqual(logic._get_priority('('), 0)
        self.assertEqual(logic._get_priority('=='), 1)
        self.assertEqual(logic._get_priority('^'), 4)

    def test_polish_notation(self):
        self.assertEqual(logic.rebuild_into_polish_notation(['2', '+', '2'],
                                               methods), ['2', '2', '+'])
        self.assertEqual(logic.rebuild_into_polish_notation(['(', '2', '*', '3', '-', '4', ')', '/', '(', '5', '+', '2', ')'],
                                               methods),
                         ['2', '3', '*', '4', '-', '5', '2', '+', '/'])

    def test_ex_calc(self):
        self.assertEqual(logic.ex_calc(['2', '2', '+'], methods), 4)
        self.assertEqual(logic.ex_calc(['2', '3', '*', '4', '5', '+', '2', '*', '4', '+', '5', '*', '+'],
                                       methods), 116)
        self.assertEqual(logic.ex_calc(['2', ['0', '2', '-'], 'abs', '+'], methods), 4)
        self.assertEqual(logic.ex_calc(['True', 'True', '+'], methods), 2)

    def test_calculate(self):
        self.assertEqual(main_funcs.calculate('-+---+-1', methods), -+---+-1)
        self.assertEqual(main_funcs.calculate('2---2', methods), 2 - --2)
        self.assertEqual(main_funcs.calculate('2+2', methods), 4)
        self.assertEqual(main_funcs.calculate('True + True', methods), 2)
        self.assertEqual(main_funcs.calculate('2*3+(((4+5)*2)+4)*5', methods), 116)
        self.assertEqual(main_funcs.calculate('5*abs(-2)/round(5.3)', methods), 2)
        self.assertEqual(main_funcs.calculate('5*abs(-2)/round(5.3)+2.2', methods), 4.2)
        self.assertEqual(main_funcs.calculate('5*abs(-2)/round(5.3)==2.2^3', methods), False)
