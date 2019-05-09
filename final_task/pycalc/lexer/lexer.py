"""
Lexer class.
"""

import re
from collections import namedtuple


Token = namedtuple("Token", ("token_type", "lexeme"))
LexerContext = namedtuple('LexerContext', ('source', 'pos'))

WHITESPACES = re.compile(r"\s+")


class Lexer:
    """Represents a lexer."""

    def __init__(self, matchers):
        self.matchers = matchers
        self.source = ''
        self.pos = 0
        self.prev_pos = 0
        self.length = 0

        # a wrapper for caching the last peeked token
        self._token_wrapper = []

    def init(self, source):
        """Init a lexer with a source string."""

        self.source = source
        self.pos = 0
        self.prev_pos = 0
        self.length = len(source)
        self._token_wrapper.clear()

    def context(self, previous=False):
        """Return a lexer context."""

        pos = self.prev_pos if previous else self.pos

        return LexerContext(self.source, pos)

    def is_source_exhausted(self):
        """Return `True` if the position pointer is out of the source string."""

        assert(self.pos) >= 0

        return self.pos >= self.length

    def peek(self):
        """"""

        if self._token_wrapper:
            return self._token_wrapper[-1]

        token = self._next_token()
        self._token_wrapper.append(token)

        return token

    def consume(self):
        """"""

        token = self.peek()
        self._token_wrapper.pop()
        if token:
            self._advance_pos_by_lexeme(token.lexeme)

        return token

    def format(self):
        """"""

        pos = self.pos
        begin = self.source[:pos]
        end = self.source[pos:]

        return f'{begin}>{end}'

    def _next_token(self):
        """Try to match the next token."""

        self._skip_whitespaces()
        token = self._match()

        return token

    def _match(self):
        """Return `Token` or `None`."""

        for token_type, matcher in self.matchers:
            lexeme = matcher(self.source, self.pos)

            if not lexeme:
                continue

            token = Token(token_type, lexeme)

            return token

    def _skip_whitespaces(self):
        """Skip whitespaces and advance the position index
        to the first non whitespace symbol."""

        whitespaces = WHITESPACES.match(self.source, self.pos)
        if whitespaces:
            self._advance_pos_by_lexeme(whitespaces.group())

    def _advance_pos_by_lexeme(self, lexeme):
        """Advance the position index by lexeme lenght."""

        value = len(lexeme)
        self.prev_pos = self.pos
        self.pos += value
