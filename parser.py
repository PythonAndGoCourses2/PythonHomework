import sys


def get_token(input_expression):
    if input_expression.count('(') != input_expression.count(')'):
        print('ERROR: the number of opening and closing brackets must match')
        sys.exit(1)
    else:
        token = ['']
        for i in input_expression:
            if i.isdigit() and token[-1].isdigit():
                token[-1] = token[-1]+i
            elif i == '.' and token[-1].isdigit():
                token[-1] = token[-1] + i
            elif i.isdigit() and '.' in token[-1]:
                token[-1] = token[-1] + i
            elif i.isalpha() and token[-1].isalpha():
                token[-1] = token[-1] + i
            elif i == '/' and token[-1] == '/':
                token[-1] = token[-1] + i
            elif i == '=' and token[-1] in '<>!=':
                token[-1] = token[-1] + i
            else:
                token.append(i)
        return token[1:]

