""""""
from pycalc.lexer.lexer import Lexer
from pycalc.matcher.matcher import matchers


class Parser:
    """"""

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = None
        self.next_token = None

    def parse(self, source):
        """"""

        self.lexer.init(source)
        self.next()

        return self.expression()

    def next(self):
        """"""

        self.token = self.next_token
        self.next_token = self.lexer.get_next_token()

    def advance(self, token_class=None):
        """"""

        if token_class and not self.next_token.is_instance(token_class):
            raise SyntaxError(f"Expected: {token_class.__name__}")

        self.next_token = self.lexer.get_next_token()

    def expression(self, rbp=0):
        """"""

        self.next()
        left = self.token.prefix()
        print('in expression start:', self.token, self.next_token, left)
        while rbp < self.next_token.lbp:
            self.next()
            left = self.token.infix(left)

        return left


if __name__ == "__main__":
    l = Lexer(matchers)
    p = Parser(l)
    assert p.parse('- - - 2 ** fn ( 1 , ( 2 + 1 ) * 5 , 4 )') == -1048576
    assert p.parse('- - 2') == 2
    assert p.parse('4 ** 3 ** 2') == 262144
    assert p.parse('1 + 2 * 3') == 7
    assert p.parse('( 1 + 2 ) * 3') == 9
    assert p.parse('1 + 2 == 3') is True
    assert p.parse('0 == 1') is False
    # TODO:
    # assert p.parse('0 1') is False
