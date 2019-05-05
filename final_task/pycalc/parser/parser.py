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
        try:
            result = self.expression()
        except Exception as e:
            print(f'{e}: (pos: {self.lexer.pos}), {self.lexer.format()}')

        assert self.lexer.source_exhausted(), \
            f'source not parsed completely, (pos: {self.lexer.pos}), {self.lexer.format()}'

        print(f'output: {result}')

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


if __name__ == "__main__":
    from pycalc.lexer.lexer import Lexer
    from pycalc.matcher.matcher import matchers
    from pycalc.specification.specification import spec

    lexer = Lexer(matchers)
    p = Parser(spec, lexer)
    assert p.parse('2') == 2
    assert p.parse('    2') == 2
    assert p.parse('- 2') == - 2
    assert p.parse('- - 2') == 2
    assert p.parse('1 - 2') == -1
    assert p.parse('    1    -    2   ') == -1
    assert p.parse('1 - - 2') == 3
    assert p.parse('1 - - - 2  ') == -1
    # assert p.parse('2 ** 3 ') == 8
    assert p.parse('1 - 2 * 3') == -5
    assert p.parse('3 ^ 2 * 2') == 18
    assert p.parse('3 * 2 ^ 2') == 12
    assert p.parse('4 ^ 3 ^ 2') == 262144
    assert p.parse('6-(-13)') == 19
    assert p.parse('( 7 - 2 ) * 3') == 15
    assert p.parse('(0)') == 0
    # assert p.parse(') 2 ') == 15
    assert p.parse('0 > 1') is False
    assert p.parse('0 >= 1') is False
    assert p.parse('2 > 1') is True
    assert p.parse('1 >= 1') is True
    assert p.parse('1 - 2 >= -1') is True
    assert p.parse('sum(1 - 3, 2 - 5)') == -5
    # assert p.parse(', 1') is True
    # assert p.parse('1 , 2') is True
    assert p.parse('- - - 2 ^ sum ( 1 , ( 4 - 1 ) * 5 , 4 )') == -1048576
    # TODO:
    # assert p.parse('0 1') is False
