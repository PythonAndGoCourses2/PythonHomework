"""
Matchers class.
"""

from collections import namedtuple

from .helpers import construct_regex, regex_matcher


Matcher = namedtuple("Matcher", ("token_type", "matcher"))


class Matchers:
    """
    Matchers is an iterable container for matchers with methods
    for creating matchers from literals list or regex.
    """

    def __init__(self):
        self.matchers = []

    def __iter__(self):
        for matcher in self.matchers:
            yield matcher

    def register_matcher(self, token_type, matcher):
        """Register a matcher with a corresponding token type."""

        self.matchers.append(Matcher(token_type, matcher))

    @staticmethod
    def create_matcher_from_regex(regex):
        """Create a matcher from compiled regex object."""

        return regex_matcher(regex)

    @staticmethod
    def create_matcher_from_literals_list(literals):
        """Create a matcher from a list of literals"""

        return regex_matcher(construct_regex(literals))
