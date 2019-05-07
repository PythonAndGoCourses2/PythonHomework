"""
Matchers class.
"""

from collections import namedtuple

from .creator import MatcherCreator


Matcher = namedtuple("Matcher", ("token_type", "matcher"))


class Matchers:
    """
    Matchers is an iterable container for matchers with methods
    for creating matchers from literals list or regex.
    """

    def __init__(self):
        self.matchers = []
        self.create_from = MatcherCreator

    def __iter__(self):
        for matcher in self.matchers:
            yield matcher

    def register_matcher(self, token_type, matcher):
        """Register a matcher with a corresponding token type."""

        self.matchers.append(Matcher(token_type, matcher))
