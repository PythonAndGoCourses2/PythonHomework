"""
Parser package provides a Parser class for
top down operator precedence parsing (Pratt parser).
"""


class Parser:
    """
     Parser class for top down operator precedence parsing (Pratt parser).
     """

    def __init__(self, spec, lexer):
        self.spec = spec
        self.lexer = lexer

    def parse(self, source):
        """"""

        self.lexer.init(source)

        try:
            result = self.expression()
        except Exception as e:
            print(
                f'ERROR: {e}: (pos: {self.lexer.pos}), {self.lexer.format()}')
            raise e

        assert self.lexer.is_source_exhausted(), \
            f'source not parsed completely, (pos: {self.lexer.pos}), {self.lexer.format()}'

        return result

    def expression(self, right_power=0):
        """"""

        token = self.consume()
        if not token:
            raise SyntaxError('i expect something but nothing finded')

        left = self._nud(token)

        while True:
            token = self.peek()
            if not token:
                break

            if right_power >= self._left_power(token):
                break

            self.consume()
            left = self._led(token, left)

        return left

    def consume(self):
        """"""

        return self.lexer.consume()

    def peek(self):
        """"""

        return self.lexer.peek()

    def advance(self, token_type=None):
        """"""

        token = self.peek()

        if not token or (
                token_type and
                not token.token_type == token_type
        ):
            raise SyntaxError(f"Expected: {token_type}")

        self.consume()

    def peek_and_check(self, token_type):
        """"""

        token = self.peek()
        if not token or token.token_type != token_type:
            return False

        return True

    def _nud(self, token):
        """"""

        return self.spec.nud.eval(self, token)

    def _led(self, token, left):
        """"""

        return self.spec.led.eval(self, token, left)

    def _left_power(self, token):
        """"""

        return self.spec.led.power(token)
