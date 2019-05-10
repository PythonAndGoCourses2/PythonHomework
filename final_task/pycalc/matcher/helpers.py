"""
Helpers function for building matchers.
"""

import re


def list_sorted_by_length(iterable) -> list:
    """
    Return a sorted list from iterable.

    Result list is sorted by length in reversed order.
    """

    return sorted(iterable, key=len, reverse=True)


def construct_literals_list(literals):
    """Return a list of literals sorted by length in reversed order."""

    sorted_literals = list_sorted_by_length(literals)
    return sorted_literals


def construct_regex(literals):
    r"""
    Return regex string for... .

    >>> construct_regex_string(['🏇', cos', 'arcsin', 'sin', pi()'])
    arcsin|pi\(\)|cos|sin|\🏇

    """

    literals_list = construct_literals_list(literals)
    regex_string = '|'.join(map(re.escape, literals_list))
    regex = re.compile(regex_string)

    return regex


def regex_matcher(regex):
    """Return a regex matcher function."""

    def matcher(string, pos):
        """
        Return a substring that match a string from
        a given position or `None` if there are no matches.
        """

        result = regex.match(string, pos)
        if result:
            return result.group()

    return matcher
