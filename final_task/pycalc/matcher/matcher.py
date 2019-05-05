
from collections import namedtuple

from pycalc.token.constants import TokenType

from .helpers import construct_regex, regex_matcher
from .number import NUMBER_MATCHER


# operation:  + - etc.                    predefined
# constants:  pi, e etc.                  load from module
# function:   sin, abs etc.               load from module
# numbers:    0, 10, 15., .03, 2.14 etc.  dynamicaly matched (no literal)
# other:      ( ) ,                       predefined

Matcher = namedtuple("Matcher", ("token_type", "matcher"))

PREDEFINED_MATCHERS = {
    TokenType.NUMERIC: NUMBER_MATCHER
}

# operators = ['+', '>', '-', '>=', '==', '<=', '!', '^']
# functions = ['sin', 'arcsin', 'abs', 'time']
# constants = ['pi', 'e', 'nan']
# punctuations = ['(', ')', ',']


class Matchers:
    def __init__(self):
        self.matchers = []

    def __iter__(self):
        for matcher in self.matchers:
            yield matcher

    def register_matcher(self, token_type, matcher):
        """"""

        self.matchers.append(Matcher(token_type, matcher))

    def create_matcher_from_regex(self, regex):
        """"""

        return regex_matcher(regex)

    def create_matcher_from_literals_list(self, literals):
        """"""

        return regex_matcher(construct_regex(literals))


matchers = Matchers()

matchers.register_matcher(TokenType.NUMERIC,
                          PREDEFINED_MATCHERS[TokenType.NUMERIC])

matchers.register_matcher(TokenType.SUB,
                          matchers.create_matcher_from_literals_list(['-']))

matchers.register_matcher(TokenType.MUL,
                          matchers.create_matcher_from_literals_list(['*']))

matchers.register_matcher(TokenType.POW,
                          matchers.create_matcher_from_literals_list(['^']))

matchers.register_matcher(TokenType.GE,
                          matchers.create_matcher_from_literals_list(['>=']))

matchers.register_matcher(TokenType.GT,
                          matchers.create_matcher_from_literals_list(['>']))

matchers.register_matcher(TokenType.LEFT_PARENTHESIS,
                          matchers.create_matcher_from_literals_list(['(']))

matchers.register_matcher(TokenType.RIGHT_PARENTHESIS,
                          matchers.create_matcher_from_literals_list([')']))

matchers.register_matcher(TokenType.SUM,
                          matchers.create_matcher_from_literals_list(['sum']))

matchers.register_matcher(TokenType.COMMA,
                          matchers.create_matcher_from_literals_list([',']))

# matchers.register_matcher(TokenType.CONSTANT,
#                           matchers.create_matcher_from_literals_list(constants))
# matchers.register_matcher(TokenType.FUNCTION,
#                           matchers.create_matcher_from_literals_list(functions))
# matchers.register_matcher(TokenType.PUNCTUATION,
#                           matchers.create_matcher_from_literals_list(punctuations))

if __name__ == '__main__':

    source = '1.3>=sin(pi+e)'
    pos = 0
    while True:
        for token_type, matcher in matchers:
            result = matcher(source, pos)
            if result:
                print(token_type, result)
                pos += len(result)
                break
        if pos >= len(source):
            break
