import unittest
import string
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

    def test_choose_category(self):
        self.assertEqual(string.whitespace, tokenizer.choose_category(' '))
        self.assertEqual(string.ascii_letters + '_', tokenizer.choose_category('t'))
        self.assertEqual(string.ascii_letters + '_', tokenizer.choose_category('_'))
        self.assertEqual(string.digits + '.', tokenizer.choose_category('5'))
        self.assertEqual(string.digits + '.', tokenizer.choose_category('.'))
        self.assertEqual('!"#$%&\'*+,-/:;<=>?@\\^`|~', tokenizer.choose_category('*'))
        self.assertEqual('!"#$%&\'*+,-/:;<=>?@\\^`|~', tokenizer.choose_category('+'))
        self.assertEqual('!"#$%&\'*+,-/:;<=>?@\\^`|~', tokenizer.choose_category('\''))
        self.assertEqual('(){}[]', tokenizer.choose_category('('))
        self.assertEqual('(){}[]', tokenizer.choose_category(')'))

    def test_prepare_string(self):
        self.assertEqual('15 + 12^2/lg(15)', tokenizer.prepare_string('15 + 12^2/log10(15)'))
        self.assertEqual('sin(pi) + 12^2/logOneP(e)', tokenizer.prepare_string('sin(pi) + 12^2/log1p(e)'))
        self.assertEqual('lgTwo(pi) - 17*lg(e)', tokenizer.prepare_string('log2(pi) - 17*log10(e)'))


class TestTranslator(unittest.TestCase):
    def test_process_close_bracket(self):
        self.assertRaises(exeptions.BracketsError, translator.process_close_bracket, ['5', ',', '10'], [])
        self.assertRaises(exeptions.BracketsError, translator.process_close_bracket, ['45', '+', ')'], [])
        self.assertEqual(None, translator.process_close_bracket(['(', '500', '('], []))

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
