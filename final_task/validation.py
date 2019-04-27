import sys
import re
import config


def empty_string(string):
    """Check for empty string."""
    if string == "":
        print('ERROR: string is empty!')
        sys.exit(1)


def only_one_character(string):
    """Single character check."""
    if len(string) == 1 and not string.isdigit() and not string == 'e':
        print('ERROR: only one character!')
        sys.exit(1)


def space_between_numbers(string):
    """
    Search for incorrect combinations in which between numbers an unlimited number of whitespace characters.

    Example: '1 2', '1 + (1 2)'.
    """
    res = re.search(r'\d+\s+\d+', string)
    if res:
        print('ERROR: space between numbers!')
        sys.exit(1)


def incorrect_number_of_brackets(string):
    """
    Checking the number of left and right brackets.

    Example: '((1+2)', '(1+2)+(1+2'
    """
    count_left = string.count('(')
    count_right = string.count(')')
    if count_left != count_right:
        print('ERROR: brackets are not balanced!')
        sys.exit(1)


def space_between_comparison_characters(string):
    """
    Search for incorrect combinations in which between the characters of the comparison an unlimited
    number of whitespace characters.

    Example: '2 > = 2', '2 < = 2'.
    """
    for token_1 in config.comparison_check:
        for token_2 in config.comparison_check:
            pattern = re.compile(token_1 + r'\s+' + token_2)
            res = pattern.search(string)
            if res is not None:
                print('ERROR: space between comparison characters!')
                sys.exit(1)


def space_between_math_characters(string):
    """
    Search for incorrect combinations in which there is an unlimited number of whitespace characters
    between mathematical operators.

    Example: '6 * * 6', '5 / / 6'.
    """
    for token_1 in config.characters:
        if token_1 == '+' or token_1 == '-':
            continue
        for token_2 in config.characters:
            if token_2 == '+' or token_2 == '-':
                continue
            pattern = re.compile('\\' + token_1 + r'\s+' + '\\' + token_2)
            res = pattern.search(string)
            if res is not None:
                print('ERROR: space between math characters!')
                sys.exit(1)


def main(string):
    """
    Calling all validation functions.
    Input: string --> exit()
    """
    empty_string(string)
    only_one_character(string)
    space_between_numbers(string)
    space_between_comparison_characters(string)
    space_between_math_characters(string)
    incorrect_number_of_brackets(string)
