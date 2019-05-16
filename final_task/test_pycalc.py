import unittest
from pycalc import tokenizer
from pycalc import translator
from pycalc import calculator
from pycalc import exeptions


class TestParser(unittest.TestCase):
    pass


class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(['lg', '(', '10', ')'], tokenizer.tokenize('log10(10)'))
        self.assertEqual(['sin', '(', '15', '/', 'e', ')', '*', '100', '^', '3'], tokenizer.tokenize('sin(15/e)*100^3'))

    def test_append_token(self):
        self.assertEqual(['(', '(', '('], tokenizer.append_token([], '((('))
        self.assertEqual(['15', 'sin'], tokenizer.append_token(['15'], 'sin'))
        self.assertEqual(['sin', '(', '('], tokenizer.append_token(['sin'], '(('))


class TestTranslator(unittest.TestCase):
    def test_dell_spaces(self):
        self.assertEqual(['+', '19', '-', '2'], translator.dell_spaces(['+', ' ', '19', ' ', '-', '2']))
        self.assertEqual(['15', '*', '4', '^', '3'], translator.dell_spaces(['15', '*', '4', '^', '3']))
        self.assertRaises(exeptions.InvalidStringError, translator.dell_spaces, ['4', ' ', '5'])

    def test_check_invalid_func(self):
        self.assertRaises(exeptions.InvalidStringError, translator.chek_invalid_func, ['sin'])
        self.assertRaises(exeptions.InvalidStringError, translator.chek_invalid_func, ['log', '15'])
        self.assertRaises(exeptions.InvalidStringError, translator.chek_invalid_func,
                          ['cos', '(', '15', ')', '*', 'abs', '10'])

    def test_is_unary(self):
        self.assertFalse(translator.is_unary(['2', '-', '1'], 1))
        self.assertTrue(translator.is_unary(['15.3', '/', '-', '3'], 2))
        self.assertTrue(translator.is_unary(['sin', '(', '-', '15', ')'], 2))
        self.assertTrue(translator.is_unary(['2', '+', '-', '1'], 2))
        self.assertTrue(translator.is_unary(['2', '+', '-', '1'], -2))
        self.assertTrue(translator.is_unary(['2', '+', '-', '1'], 0))
        self.assertRaises(exeptions.GeneralError, translator.is_unary, ['-', '2'], 15)

    def test_make_unarys(self):
        self.assertEqual(['3', '+', '~', '1'], translator.make_unarys(['3', '+', '-', '1']))
        self.assertEqual(['3', '/', '~', '1'], translator.make_unarys(['3', '/', '-', '1']))
        self.assertEqual(['(', '19', '+', '40', ')', '-', '100'],
                         translator.make_unarys(['(', '19', '+', '40', ')', '-', '100']))

    def test_is_number(self):
        self.assertTrue(translator.is_number('10'))
        self.assertTrue(translator.is_number('10.0'))
        self.assertFalse(translator.is_number('p'))
        self.assertFalse(translator.is_number('prev.next'))

    def test_make_valid(self):
        self.assertEqual(['#', '19', '/', '~', '2'],
                         translator.make_valid(['+', ' ', '19', ' ', '/', '-', '2']))
        self.assertEqual(['~', 'sin', '(', '15', ')', '==', '~', '15'],
                         translator.make_valid(['-', 'sin', '(', '15', ')', '==', '-', '15']))
        self.assertRaises(exeptions.InvalidStringError, translator.make_valid, ['cos', '15'])

    def test_get_postfix(self):
        self.assertEqual([1.0, 1.0, '+'], translator.get_postfix(['1', '+', '1']))
        self.assertEqual([10.0, 'sin'], translator.get_postfix(['sin', '(', '10', ')']))
        self.assertEqual([30.0, 15.0, 2.0, '^', '+'], translator.get_postfix(['30', '+', '15', '^', '2']))


class TestCalculator(unittest.TestCase):
    def test_calc(self):
        self.assertEqual(2.0, calculator.calculate(['1', '1', '+']))
        self.assertRaises(ZeroDivisionError, calculator.calculate, ['15', '0', '/'])
        self.assertRaises(OverflowError, calculator.calculate, ['100', '100', '^', '100', '^', '100', '^', '100', '^'])
        self.assertRaises(exeptions.InvalidStringError, calculator.calculate, ['+'])
        self.assertRaises(exeptions.InvalidStringError, calculator.calculate, ['15', '+', '15'])


if __name__ == '__main__':
    unittest.main()
