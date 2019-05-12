import unittest
from pycalc import Tokenizer
from pycalc import Translator
from pycalc import Calculator
from pycalc import Exeptions


class TestParser(unittest.TestCase):
    pass


class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(['(', '(', '('], Tokenizer.tokenize('((('))
        self.assertEqual(['lg', '(', '10', ')'], Tokenizer.tokenize('log10(10)'))
        self.assertEqual(['+', ' ', '17'], Tokenizer.tokenize('- - 17'))


class TestTranslator(unittest.TestCase):
    def test_dell_spaces(self):
        self.assertEqual(['+', '19', '-', '2'], Translator.dell_spaces(['+', ' ', '19', ' ', '-', '2']))
        # self.assertRaises(Exeptions.InvalidStringError, Translator.dell_spaces, ['4', ' ', '5'])


    def test_check_invalid_func(self):
        pass

    def test_is_unary(self):
        self.assertFalse(Translator.is_unary(['2', '-', '1'], 1))
        self.assertTrue(Translator.is_unary(['2', '+', '-', '1'], 2))

    def test_make_unarys(self):
        self.assertEqual(['3', '+', '0', '-', '1'], Translator.make_unarys(['3', '+', '-', '1']))
        self.assertEqual(['3', '/', '(', '0', '-', '1', ')'], Translator.make_unarys(['3', '/', '-', '1']))

    def test_is_number(self):
        self.assertTrue(Translator.is_number('10'))
        self.assertTrue(Translator.is_number('10.0'))
        self.assertFalse(Translator.is_number('p'))

    def test_get_postfix(self):
        self.assertEqual(['1', '1', '+'], Translator.get_postfix(['1', '+', '1']))
        self.assertEqual(['10', 'sin'], Translator.get_postfix(['sin', '(', '10', ')']))
        self.assertEqual(['30', '15', '2', '^', '+'], Translator.get_postfix(['30', '+', '15', '^', '2']))


class TestCalculator(unittest.TestCase):
    def test_calc(self):
        self.assertEqual(2.0, Calculator.calc(['1', '1', '+']))


if __name__ == '__main__':
    unittest.main()
