import operator

OPERATORS = {'+': operator.add, '-': operator.sub,
             '*': operator.mul, '/': operator.truediv,
             '//': operator.floordiv, '%': operator.mod,
             '^': operator.pow, 'neg': operator.neg(),
             'pos': operator.pos()}

def calc(polish):
    stack = []
    for token in polish:
        if token in OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(OPERATORS[token](x, y))
        else:
            stack.append(float(token))
    return stack[0]