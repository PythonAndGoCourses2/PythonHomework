import unittest
from pycalc import Tokenizer
from pycalc import Translator
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


if __name__ == '__main__':
    unittest.main()
