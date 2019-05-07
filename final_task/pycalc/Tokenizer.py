import string

lower = string.ascii_lowercase
digits = string.digits
space = string.whitespace
punctuation = '!"#$%&\'*+,-./:;<=>?@\\^_`|~'
brackets = '(){}[]'
categories = [lower, digits, space, punctuation, brackets]


def tokenize(string):
    global categories
    token = ''
    tokens = []
    category = None
    for char in string:
        if token:
            if category and char in category:
                token += char
            else:
                tokens.append(token)
                token = char
                category = None
                for cat in categories:
                    if char in cat:
                        category = cat
                        break
        else:
            category = None
            if not category:
                for cat in categories:
                    if char in cat:
                        category = cat
                        break
            token += char
    if token:
        tokens.append(token)
    return tokens
