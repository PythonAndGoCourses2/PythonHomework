import unittest
from . import parser


class TestParser(unittest.TestCase):
    def test_get_token(self):
        self.assertEqual(parser.get_token('-13'), ['-', '13'],)
        self.assertEqual(parser.get_token('666'), ['666'])
        self.assertEqual(parser.get_token('sin(pi/2)'), ['sin', '(', 'pi', '/', '2', ')'])
        self.assertEqual(parser.get_token('4//2'), ['4', '//', '2'])
        self.assertEqual(parser.get_token('6-(-13)'), ['6', '-', '(', '-', '13', ')'])
        self.assertRaises(Exception, parser.get_token('(()'))
        self.assertRaises(Exception, parser.get_token(''))

    def test_separate_function(self):
        self.assertEqual(parser.separate_function(['sin', '(', 'pi', '/', '2', ')']), ['sin', '[', 'pi', '/', '2', ']'])

    def test_create_infix_expression(self):
        self.assertEqual(parser.create_infix_expression(['sin', '[', 'pi', '/', '2', ']']),
                         ['sin', '[', 'pi', '/', 2.0, ']'])
        self.assertEqual(parser.create_infix_expression(['.1']), [0.1])

    def test_parse_input_string(self):
        self.assertEqual(parser.parse_input_string('sin(pi/2)'), ['sin', '[', 'pi', '/', 2.0, ']'])


if __name__ == '__main__':
    unittest.main()
