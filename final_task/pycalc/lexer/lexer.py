from pycalc.token.builder import build_token


class Lexer:
    def __init__(self, source):
        self.source = source
        self.matchers = []
        self.pos = 0
        self.length = len(source)

    def _advance_pos(self, value):
        """"""

        self.pos += value

    def get_next_token(self):
        """"""

        if self.pos >= self.length:
            return EOF

        for matcher in self.matchers:
            result = matcher(self.source, self.pos)

            if not result:
                continue

            (lexeme, token_type) = result
            token = build_token(lexeme, token_type)

            self._advance_pos(len(lexeme))

            return token

    raise Exception('No match')
