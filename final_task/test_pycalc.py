import unittest
from pycalc import tokenizer
from pycalc import translator
from pycalc import calculator
from pycalc import exeptions


class TestParser(unittest.TestCase):
    pass


class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(['(', '(', '('], tokenizer.tokenize('((('))
        self.assertEqual(['lg', '(', '10', ')'], tokenizer.tokenize('log10(10)'))
        self.assertEqual(['+', ' ', '17'], tokenizer.tokenize('- - 17'))


class TestTranslator(unittest.TestCase):
    def test_dell_spaces(self):
        self.assertEqual(['+', '19', '-', '2'], translator.dell_spaces(['+', ' ', '19', ' ', '-', '2']))
        self.assertRaises(exeptions.InvalidStringError, translator.dell_spaces, ['4', ' ', '5'])

    def test_check_invalid_func(self):
        self.assertRaises(exeptions.InvalidStringError, translator.chek_invalid_func, ['sin'])
        self.assertRaises(exeptions.InvalidStringError, translator.chek_invalid_func, ['log', '15'])

    def test_is_unary(self):
        self.assertFalse(translator.is_unary(['2', '-', '1'], 1))
        self.assertTrue(translator.is_unary(['2', '+', '-', '1'], 2))

    def test_make_unarys(self):
        self.assertEqual(['3', '+', '0', '-', '1'], translator.make_unarys(['3', '+', '-', '1']))
        self.assertEqual(['3', '/', '(', '0', '-', '1', ')'], translator.make_unarys(['3', '/', '-', '1']))

    def test_is_number(self):
        self.assertTrue(translator.is_number('10'))
        self.assertTrue(translator.is_number('10.0'))
        self.assertFalse(translator.is_number('p'))

    def test_get_postfix(self):
        self.assertEqual([1.0, 1.0, '+'], translator.get_postfix(['1', '+', '1']))
        self.assertEqual([10.0, 'sin'], translator.get_postfix(['sin', '(', '10', ')']))
        self.assertEqual([30.0, 15.0, 2.0, '^', '+'], translator.get_postfix(['30', '+', '15', '^', '2']))


class TestCalculator(unittest.TestCase):
    def test_calc(self):
        self.assertEqual(2.0, calculator.calc(['1', '1', '+']))


if __name__ == '__main__':
    unittest.main()
