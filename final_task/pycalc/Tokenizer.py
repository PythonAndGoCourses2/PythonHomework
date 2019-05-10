import string

lower = string.ascii_lowercase
digits = string.digits + '.'
space = string.whitespace
punctuation = '!"#$%&\'*+,-/:;<=>?@\\^_`|~'
brackets = '(){}[]'
categories = [lower, digits, space, punctuation, brackets]


def tokenize(expression):
    global categories
    token = ''
    tokens = []
    category = None
    expression = expression.replace(' ', '')
    expression = expression.replace('log10', 'lg')
    for char in expression:
        if token:
            if category and char in category:
                token += char
            else:
                if '+' in token or '-' in token or ')' in token:
                    for c in token:
                        tokens.append(c)
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
        if '+' in token or '-' in token or ')' in token:
            for c in token:
                tokens.append(c)
        else:
            tokens.append(token)
    return tokens
