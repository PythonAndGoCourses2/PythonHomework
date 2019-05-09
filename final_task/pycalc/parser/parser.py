"""
Parser package provides a Parser class for
top down operator precedence parsing (Pratt parser).
"""


from .errors import (
    ParserExpectedTokenAbsent,
    ParserNoTokenReceived,
    ParserGenericError,
    ParserSourceNotExhausted
)


class Parser:
    """Parser class for top down operator precedence parsing (Pratt parser)."""

    def __init__(self, spec, lexer, default_power):
        self.spec = spec
        self.lexer = lexer
        self.default_power = default_power

    def parse(self, source):
        """Parse a source and return a result of parsing."""

        self.lexer.init(source)

        try:
            result = self._parse()
        except Exception as exc:
            raise ParserGenericError(self.context()) from exc

        return result

    def _parse(self):
        """The inner parsing function.

        Splitted from the main parsing function to allow
        catching all parsing error exceptions in one place.
        """

        result = self.expression()

        if not self.lexer.is_source_exhausted():
            raise ParserSourceNotExhausted(self.context())

        return result

    def expression(self, right_power=None):
        """The main parsing function of Pratt parser."""

        token = self.consume()
        if not token:
            raise ParserNoTokenReceived(self.context())

        left = self._nud(token)

        while True:
            token = self.peek()
            if not token:
                break

            right_power = right_power if right_power is not None else self.default_power
            if right_power >= self._left_power(token):
                break

            self.consume()
            left = self._led(token, left)

        return left

    def consume(self):
        """Return the next token and advance the source position pointer."""

        return self.lexer.consume()

    def peek(self):
        """Return the next token without advancing the source position pointer."""

        return self.lexer.peek()

    def advance(self, token_type=None):
        """
        Consume a next token if that one is of given type.

        Raise an `ParserExpectedTokenAbsent` exception if types don’t match.
        """

        token = self.peek()

        if not token or (
                token_type and
                not token.token_type == token_type
        ):
            raise ParserExpectedTokenAbsent(self.context())

        self.consume()

    def peek_and_check(self, token_type):
        """Check if the next token is of given type."""

        token = self.peek()
        if not token or token.token_type != token_type:
            return False

        return True

    def context(self, previous=False):
        """Return parsing context."""

        return self.lexer.context(previous)

    def _nud(self, token):
        """"""

        return self.spec.nud.eval(self, token)

    def _led(self, token, left):
        """"""

        return self.spec.led.eval(self, token, left)

    def _left_power(self, token):
        """Get token binding power."""

        return self.spec.led.power(token)
