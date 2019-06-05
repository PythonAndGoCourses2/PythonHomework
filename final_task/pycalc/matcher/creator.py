"""
Matcher creator class holds functions for matchers creation.
"""

from .helpers import regex_matcher, construct_regex


class MatcherCreator:
    """Matcher creator class holds functions for matchers creation."""

    @staticmethod
    def compiled_regex(regex):
        """Create a matcher from compiled regex object."""

        return regex_matcher(regex)

    @staticmethod
    def literals_list(literals):
        """Create a matcher from a list of literals."""

        return regex_matcher(construct_regex(literals))
