import sys
import re
import config


def empty_string(string):
    if string == "":
        sys.exit('ERROR: string is empty!')


def only_one_character(string):
    if len(string) == 1 and not string.isdigit() and not string == 'e':
        sys.exit('ERROR: only one character!')


def space_between_numbers(string):
    res = re.search(r'\d+\s+\d+', string)
    if res:
        sys.exit('ERROR: space between numbers!')


def incorrect_number_of_brackets(string):
    count_left = string.count('(')
    count_right = string.count(')')
    if count_left != count_right:
        sys.exit('ERROR: brackets are not balanced!')


def space_between_comparison_characters(string):
    for token_1 in config.comparison_check:
        for token_2 in config.comparison_check:
            pattern = re.compile(token_1 + r'\s+' + token_2)
            res = pattern.search(string)
            if res is not None:
                sys.exit('ERROR: space between comparison characters!')


def space_between_math_characters(string):
    for token_1 in config.characters:
        if token_1 == '+' or token_1 == '-':
            continue
        for token_2 in config.characters:
            if token_2 == '+' or token_2 == '-':
                continue
            pattern = re.compile('\\' + token_1 + r'\s+' + '\\' + token_2)
            res = pattern.search(string)
            if res is not None:
                sys.exit('ERROR: space between math characters!')


def main(string):
    empty_string(string)
    only_one_character(string)
    space_between_numbers(string)
    space_between_comparison_characters(string)
    space_between_math_characters(string)
    incorrect_number_of_brackets(string)
