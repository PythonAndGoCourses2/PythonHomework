"""Contains categories for tokens and tokenize function"""
import string

NUMERIC = string.digits + '.'
PUNCTUATION = '!"#$%&\'*+,-/:;<=>?@\\^_`|~'
BRACKETS = '(){}[]'
CATEGORIES = [
    string.ascii_lowercase,
    NUMERIC,
    string.whitespace,
    PUNCTUATION,
    BRACKETS
]


def tokenize(expression):
    """Returns list of tokens from input string"""
    token = ''
    tokens = []
    category = None
    expression = prepare_string(expression)
    for char in expression:
        if token:
            if category and char in category:
                token += char
            else:
                tokens = append_token(tokens, token)
                token = char
                category = choose_category(char)
        else:
            category = choose_category(char)
            token += char
    if token:
        tokens = append_token(tokens, token)
    return tokens


def choose_category(char):
    """Just choose category from CATEGORIES for char"""
    for cat in CATEGORIES:
        if char in cat:
            return cat


def prepare_string(expression):
    """Prepare expression to tokenize"""
    return expression.replace('log10(', 'lg(')


def append_token(tokens, token):
    """append token to tokens"""
    if '+' in token or '-' in token or ')' in token or '(' in token:
        for char in token:  # if token contains multy +, - or () characters, split it
            tokens.append(char)
    else:
        tokens.append(token)
    return tokens
