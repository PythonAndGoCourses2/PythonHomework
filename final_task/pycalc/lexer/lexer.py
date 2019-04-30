""""""

import re
from collections import namedtuple

from pycalc.token.constants import TokenType
from pycalc.matcher.matcher import matchers


Token = namedtuple('Token', ('token_type', 'lexeme'))
WHITESPACES = re.compile('\s+')


class Lexer:
    def __init__(self, source, matchers):
        self.source = source
        self.matchers = matchers
        self.pos = 0
        self.length = len(source)

    def get_next_token(self):
        """"""
        self._skip_whitespaces()

        if self._check_source_end():
            raise Exception('EOL')

        token = self._next_token()

        if not token:
            raise Exception('No match')

        self._advance_pos_by_lexeme(token.lexeme)

        return token

    def _next_token(self):
        """"""

        for token_type, matcher in self.matchers:
            lexeme = matcher(self.source, self.pos)

            if not lexeme:
                continue

            token = Token(token_type, lexeme)

            return token

    def _skip_whitespaces(self):
        """"""

        whitespaces = WHITESPACES.match(self.source, self.pos)
        if whitespaces:
            self._advance_pos_by_lexeme(whitespaces.group())

    def _advance_pos_by_lexeme(self, lexeme):
        """"""

        value = len(lexeme)
        self.pos += value

    def _check_source_end(self):
        """"""

        return self.pos >= self.length


if __name__ == '__main__':

    source = '  1.3 >=sin(pi   +e)  '
    l = Lexer(source, matchers)
    while True:
        print(l.get_next_token())
