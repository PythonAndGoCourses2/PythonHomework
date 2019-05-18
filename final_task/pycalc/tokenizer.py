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
    category = []
    expression = prepare_string(expression)
    for char in expression:
        if token:
            if category and char in category:
                token += char
            else:
                append_token(token, tokens)
                token = char
                category = choose_category(char)
        else:
            category = choose_category(char)
            token += char
    if token:
        append_token(token, tokens)
    return tokens


def choose_category(char):
    """Just choose category from CATEGORIES for char"""
    for category in CATEGORIES:
        if char in category:
            return category
    return None


def prepare_string(expression):
    """Prepare expression to tokenize"""
    expression = expression.replace('log10(', 'lg(')
    expression = expression.replace('log2(', 'lgTwo(')
    return expression


def append_token(token: str, tokens: list):
    """append token to tokens"""
    if '+' in token or '-' in token or ')' in token or '(' in token:
        for char in token:  # if token contains multy +, - or () characters, split it
            tokens.append(char)
    else:
        tokens.append(token)
