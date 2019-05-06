"""
"""

from collections import namedtuple

from .helpers import construct_regex, regex_matcher


Matcher = namedtuple("Matcher", ("token_type", "matcher"))


class Matchers:
    """"""

    def __init__(self):
        self.matchers = []

    def __iter__(self):
        for matcher in self.matchers:
            yield matcher

    def register_matcher(self, token_type, matcher):
        """"""

        self.matchers.append(Matcher(token_type, matcher))

    @staticmethod
    def create_matcher_from_regex(regex):
        """"""

        return regex_matcher(regex)

    @staticmethod
    def create_matcher_from_literals_list(literals):
        """"""

        return regex_matcher(construct_regex(literals))
