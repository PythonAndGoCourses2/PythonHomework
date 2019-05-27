input_expression = "-sin(-3.0^5.0)"

token = ['']

for i in input_expression.replace(" ", ""):
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
    else:
        token.append(i)
print(token[1:])
