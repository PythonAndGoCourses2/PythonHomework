"""
Parser.
"""


class Parser:
    """"""

    def __init__(self, registry, lexer):
        self.registry = registry
        self.lexer = lexer

    def parse(self, source):
        """"""

        self.lexer.init(source)
        result = self.expression()

        assert self.lexer.source_exhausted(), \
            f'Unparsed part of source left, (pos: {self.lexer._pos}).'

        return result

    def expression(self, power=0):
        """"""

        token = self.consume()
        if not token:
            raise Exception('i expect something but nothing finded')

        left = token.nud()

        while True:
            token = self.peek()
            if not token:
                break

            if power >= token.power.led:
                break

            self.consume()
            left = token.led(left)

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
