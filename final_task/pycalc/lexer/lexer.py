""""""

import re
from collections import namedtuple

from pycalc.token.constants import TokenType
# from pycalc.matcher.matcher import matchers


Token = namedtuple("Token", ("token_type", "lexeme"))
WHITESPACES = re.compile("\s+")


class Lexer:
    def __init__(self, matchers):
        self.matchers = matchers
        self._source = ""
        self._pos = 0
        self._length = 0

    def init(self, source):
        self._source = source
        self._pos = 0
        self._length = len(source)

    def get_next_token(self):
        """"""
        self._skip_whitespaces()

        if self._is_source_exhausted():
            raise Exception("EOL")

        token = self._next_token()

        if not token:
            raise Exception("No match")

        self._advance_pos_by_lexeme(token.lexeme)

        return token

    def _next_token(self):
        """"""

        for token_type, matcher in self.matchers:
            lexeme = matcher(self._source, self._pos)

            if not lexeme:
                continue

            token = Token(token_type, lexeme)

            return token

    def _skip_whitespaces(self):
        """"""

        whitespaces = WHITESPACES.match(self._source, self._pos)
        if whitespaces:
            self._advance_pos_by_lexeme(whitespaces.group())

    def _advance_pos_by_lexeme(self, lexeme):
        """"""

        value = len(lexeme)
        self._pos += value

    def _is_source_exhausted(self):
        """"""

        return self._pos >= self._length


if __name__ == "__main__":

    source = "  1.3 >=sin(pi   +e)  "
    l = Lexer(matchers)
    l.init(source)
    while True:
        print(l.get_next_token())
