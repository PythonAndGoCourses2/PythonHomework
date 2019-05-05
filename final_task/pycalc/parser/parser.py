"""
Parser.
"""


class Parser:
    """"""

    def __init__(self, spec, lexer):
        self.spec = spec
        self.lexer = lexer

    def parse(self, source):
        """"""

        print('=' * 30)
        print(f'input : {source}')

        self.lexer.init(source)
        result = self.expression()

        assert self.lexer.source_exhausted(), \
            f'Unparsed part of source left, (pos: {self.lexer._pos}).'

        print(f'output: {result}')

        return result

    def expression(self, right_power=0):
        """"""

        token = self.consume()
        if not token:
            raise Exception('i expect something but nothing finded')

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

    def advance(self, token_class=None):
        """"""

        token = self.peek()

        if not token or (
                token_class and
                not token.is_instance(token_class)
        ):
            raise SyntaxError(f"Expected: {token_class.__name__}")

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


if __name__ == "__main__":
    from pycalc.lexer.lexer import Lexer
    from pycalc.matcher.matcher import matchers

    l = Lexer(matchers)
    p = Parser(None, l)
    assert p.parse('2') == 2
    assert p.parse('- 2') == 2
    assert p.parse('- - 2') == 2
    assert p.parse('1 - - 2') == 3
    assert p.parse('4 ** 3 ** 2') == 262144
    assert p.parse('1 + 2 * 3') == 7
    assert p.parse('( 1 + 2 ) * 3') == 9
    assert p.parse('1 + 2 == 3') is True
    assert p.parse('0 == 1') is False
    assert p.parse('- - - 2 ** fn ( 1 , ( 2 + 1 ) * 5 , 4 )') == -1048576
    # TODO:
    # assert p.parse('0 1') is False
