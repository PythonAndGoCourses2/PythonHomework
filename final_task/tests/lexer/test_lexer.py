import unittest

from pycalc.lexer.lexer import Lexer


class InitTestCase(unittest.TestCase):

    def test_class_init(self):
        '''Test class __init__() method'''

        matchers = ['1']
        source = 'some_source'
        lexer = Lexer(matchers, source)

        self.assertEqual(lexer.source, source)
        self.assertEqual(lexer.matchers, matchers)
        self.assertEqual(lexer.pos, 0)
        self.assertEqual(lexer.length, len(source))

    def test_is_source_exhausted(self):
        """"""

        lexer = Lexer([], '')
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
                lexer = Lexer([], '')
                lexer.pos = pos
                lexer.length = length
                self.assertEqual(lexer.is_source_exhausted(),
                                 expected_result)

    @unittest.skip('not implemented')
    def test_peek(self):
        pass

    @unittest.skip('not implemented')
    def test_consume(self):
        pass

    @unittest.skip('not implemented')
    def test__next_token(self):
        pass

    @unittest.skip('not implemented')
    def test__match(self):
        pass

    def test__skip_whitespaces(self):
        """"""

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
                lexer = Lexer([], source)
                lexer.pos = pos
                lexer._skip_whitespaces()
                self.assertEqual(lexer.pos, expected_pos)

    def test__advance_pos_by_lexeme(self):
        """"""

        lexeme = 'abcde'
        pos = 10
        expected_pos = pos + len(lexeme)

        lexer = Lexer([], '')
        lexer.pos = pos

        lexer._advance_pos_by_lexeme(lexeme)
        self.assertEqual(lexer.pos, expected_pos)


if __name__ == '__main__':
    unittest.main()
