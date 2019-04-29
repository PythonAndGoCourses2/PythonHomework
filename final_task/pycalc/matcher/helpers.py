""""""

import re


def list_sorted_by_length(iterable) -> list:
    """"""

    return sorted(iterable, key=len, reverse=True)


def construct_literals_list(literals):
    """"""

    sorted_literals = list_sorted_by_length(literals)
    return sorted_literals


def construct_regex(literals):
    """Return regex string for... .

    >>> construct_regex_string(['🏇', cos', 'arcsin', 'sin', pi()'])
    arcsin|pi\(\)|cos|sin|\🏇

    """

    literals_list = construct_literals_list(literals)
    regex_string = '|'.join(map(re.escape, literals_list))
    regex = re.compile(regex_string)

    return regex


def regex_matcher(regex):
    """"""

    def matcher(string, pos):
        """"""
        result = regex.match(string, pos)
        if result:
            return result.group()

    return matcher


def text_matcher(literals):
    """"""

    def matcher(string, pos):
        """"""

        for literal in literals:
            if string.startswith(literal, pos):
                return literal

    return matcher
