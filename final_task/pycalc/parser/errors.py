"""
Exceptions for the parser package.
"""

GENERIC_PARSER_ERROR = 'encountered an error while parsing'
GENERIC_PARSER_SYNTAX_ERROR = 'syntax error'


class ParserGenericError(SyntaxError):
    """A generic exception for a parser."""

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    def __str__(self):
        return GENERIC_PARSER_ERROR


class ParserSyntaxError(ParserGenericError):
    """A generic parser exception that represents a syntax error."""

    def __str__(self):
        return GENERIC_PARSER_SYNTAX_ERROR


class ParserNoTokenReceived(ParserGenericError):
    """Raise when a lexer returns `None` instead of `Token` object."""

    pass


class ParserExpectedTokenAbsent(ParserGenericError):
    """Raise when a token is not of a given type."""

    pass


class ParserSourceNotExhausted(ParserGenericError):
    """
    Raise when a parser finished parsing a source
    but a source is not parsed completely.
    """

    pass
