# -*- coding: utf-8 -*-
"""
The module is a regular expression library for searching math expressions.

Attributes:
    REGEXP_DIGIT (rstr): regular expressions for finding numbers.
    REGEXP_SIMPLE_DIGIT (rstr): regular expressions for checking common digits.
    REGEXP_SCREENING (rstr): regular expressions for operation screening.
    REGEX_NAME (rstr): regular expressions for finding names.
    REGEXP_BACKETS (rstr): regular expressions for finding brackets.
    REGEXP_FUNCTION (rstr): regular expressions for finding functons.
    REGEXP_CONSTANT (rstr): regular expressions for finding constant names.
    REGEXP_UNARY (rstr): regular expressions for finding unary operation.
    REGEXP_BYNARY (rstr): regular expressions for finding bynary operation.
    REGEXP_COMPARE (rstr): regular expressions for finding compare operation.
    REGEXP_NON_ZERO_FRACTION_PART (rstr): regular expressions for finding non-zero fraction part.
    REGEXP_COMPARATOR (rstr): regular expressions for finding comparator.
    REGEXP_INCORECT_EXPRETION (rstr): regular expressions for defining invalid expressions.
    
"""

import re

REGEXP_DIGIT = r'[+-]?\d+\.\d+e\+\d+|[+-]?\d+\.?\d*|[+-]?\d*\.?\d+'
REGEXP_SIMPLE_DIGIT = rf'^({REGEXP_DIGIT})$'
REGEXP_SCREENING = rf'\{{operation}}'
REGEX_NAME = r'\w+'
REGEXP_BACKETS = r'(?:^|\W)(\([^)(]+\))'
REGEXP_FUNCTION = rf'(?P<pattern>(?P<name>{REGEX_NAME})\((?P<args>(?:{REGEXP_DIGIT})(?:,(?:{REGEXP_DIGIT})+)*|)\))'
REGEXP_CONSTANT = rf'(?P<name>{REGEXP_DIGIT}|{REGEX_NAME}\(?)'
REGEXP_UNARY = rf'([-+]{{2,}})'
REGEXP_BYNARY = rf'((?:{REGEXP_DIGIT})(?:{{operation}}(?:{REGEXP_DIGIT}))+)'
REGEXP_COMPARE = rf'^{REGEXP_BYNARY}$'.format(operation='[=!<>]{1,2}')
REGEXP_NON_ZERO_FRACTION_PART = r'\.0*[1-9]'
REGEXP_COMPARATOR = r'[=!<>]{1,2}'
REGEXP_INCORECT_EXPRETION = (
    r'.?\W\d+\s*\(|'
    r'^\d+\s*\(|'
    r'^\W*$|'
    r'\d+[)(<=!>][<>!]\d+|'
    r'\W\d+[)(<=!>][<!>]\d+|'
    r'\w+\s+\w+|'
    r'[-+*^\/%<=!>]+\s+[\/*^%<=!>]+|'
    r'^[\/*^%<=!>]|'
    r'[-+*^\/%<=!>]$'
)

def has_comparator(expr):
    match = re.search(REGEXP_COMPARATOR, expr)
    return bool(match)

def has_non_zero_fraction_part(expr):
    match = re.search(REGEXP_NON_ZERO_FRACTION_PART, expr)
    return bool(match)