OPETATIONS = {'+': 1, '-': 1, '*': 2, '/': 2, '//': 2, '%': 2, '^': 3}

def sort(token):
    stack = []
    for i in token:
        if i in OPETATIONS:
            while stack and stack[-1] != ('(') and OPETATIONS[token][0] <= OPETATIONS[stack[-1]][0]:
                stack.pop()
            stack.append(i)
        elif i == ')':