import logic
import constants
import unittest
import pycodestyle
import mainclass

pycodestyle.maximum_line_length = 120

logic.import_usr_imports(constants.imports)

pycalc = mainclass.PyCalc(['user_import_test_case'])


class LogicTests(unittest.TestCase):

    def test_get_item_by_type(self):
        self.assertEqual(logic._get_item_by_type('2', logic.get_imports_attrs(constants.imports)), 2)
        self.assertEqual(logic._get_item_by_type('2.4', logic.get_imports_attrs(constants.imports)), 2.4)
        self.assertEqual(logic._get_item_by_type('True', logic.get_imports_attrs(constants.imports)), True)

    def test_str_parse(self):
        self.assertEqual(logic.str_parse('2+2'), ['2', '+', '2'])
        self.assertEqual(logic.str_parse('5+abs(-5)'), ['5', '+', 'abs', '(', '0', '-', '5', ')'])

    def test_priority(self):
        self.assertEqual(logic._priority('+'), 2)
        self.assertEqual(logic._priority('*'), 3)
        self.assertEqual(logic._priority('('), 0)
        self.assertEqual(logic._priority('=='), 1)
        self.assertEqual(logic._priority('^'), 4)

    def test_polish_notation(self):
        self.assertEqual(logic.polish_notation(['2', '+', '2'],
                                               logic.get_imports_attrs(constants.imports)), ['2', '2', '+'])
        self.assertEqual(logic.polish_notation(['(', '2', '*', '3', '-', '4', ')', '/', '(', '5', '+', '2', ')'],
                                               logic.get_imports_attrs(constants.imports)),
                         ['2', '3', '*', '4', '-', '5', '2', '+', '/'])
        self.assertEqual(logic.polish_notation(['(', '2', '+', '3', ')', '/', 'abs', '(', '-', '5', ')', '-', 'sqrt', '(', '4', ')'],
                                               logic.get_imports_attrs(constants.imports)),
                         ['2', '3', '+', '5', '-', 'abs', '/', '4', 'sqrt', '-'])

    def test_ex_calc(self):
        self.assertEqual(logic.ex_calc(['2', '2', '+'], logic.get_imports_attrs(constants.imports)), 4)
        self.assertEqual(logic.ex_calc(['2', '3', '*', '4', '5', '+', '2', '*', '4', '+', '5', '*', '+'],
                                       logic.get_imports_attrs(constants.imports)), 116)
        self.assertEqual(logic.ex_calc(['2', '0', '2', '-', 'abs', '+'], logic.get_imports_attrs(constants.imports)), 4)
        self.assertEqual(logic.ex_calc(['True', 'True', '+'], logic.get_imports_attrs(constants.imports)), 2)

    def test_calculate(self):
        self.assertEqual(pycalc.calculate('2+2'), 4)
        self.assertEqual(pycalc.calculate('True + True'), 2)
        self.assertEqual(pycalc.calculate('2*3+(((4+5)*2)+4)*5'), 116)
        self.assertEqual(pycalc.calculate('5*abs(-2)/round(5.3)'), 2)
        self.assertEqual(pycalc.calculate('5*abs(-2)/round(5.3)+2.2'), 4.2)
        self.assertEqual(pycalc.calculate('5*abs(-2)/round(5.3)==2.2^3'), False)
        self.assertEqual(pycalc.calculate('sin(4)'), 4)
