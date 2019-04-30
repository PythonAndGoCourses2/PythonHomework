import unittest

from pycalc.lexer.lexer import Lexer


class InitTestCase(unittest.TestCase):

    def test_class_init(self):
        '''Test class __init__() method'''

        matchers = ['1']
        lexer = Lexer(matchers)

        self.assertEqual(lexer._source, '')
        self.assertEqual(lexer.matchers, matchers)
        self.assertEqual(lexer._pos, 0)
        self.assertEqual(lexer._length, 0)

    def test_init(self):
        """"""

        matchers = ['1']
        source = 'non_empty_string'

        lexer = Lexer(matchers)
        lexer._source = source * 2  # arbitrary number
        lexer._pos += 13            # arbitrary number
        lexer._length += 13         # arbitrary number

        lexer.init(source)
        self.assertEqual(lexer._source, source)
        self.assertEqual(lexer._pos, 0)
        self.assertEqual(lexer._length, len(source))

    @unittest.skip('not implemented')
    def test_get_next_token(self):
        pass

    @unittest.skip('not implemented')
    def test__next_token(self):
        pass

    def test__skip_whitespaces(self):
        """"""

        lexer = Lexer([])
        test_cases = (
            (' bcd', 0, 1),
            ('  cd', 0, 2),
            ('0  d', 1, 3),
            (' ', 0, 1),
            ('', 0, 0),
            ('\n\tc', 0, 2),
        )

        for source, pos, expected_pos in test_cases:
            with self.subTest(source=source,
                              pos=pos,
                              expected_pos=expected_pos):
                lexer.init(source)
                lexer._pos = pos
                lexer._skip_whitespaces()
                self.assertEqual(lexer._pos, expected_pos)

    def test__advance_pos_by_lexeme(self):
        """"""

        lexeme = 'abcde'
        pos = 10
        expected_pos = pos + len(lexeme)

        lexer = Lexer([])
        lexer._pos = pos

        lexer._advance_pos_by_lexeme(lexeme)
        self.assertEqual(lexer._pos, expected_pos)

    def test__check_source_end(self):
        """"""

        lexer = Lexer([])
        test_cases = (
            (0, 0, True),
            (3, 3, True),
            (1, 2, False),
            (2, 1, True),
        )

        for pos, length, expected_result in test_cases:
            with self.subTest(pos=pos,
                              length=length,
                              expected_result=expected_result
                              ):
                lexer = Lexer([])
                lexer._pos = pos
                lexer._length = length
                self.assertEqual(lexer._is_source_exhausted(),
                                 expected_result)


if __name__ == '__main__':
    unittest.main()
