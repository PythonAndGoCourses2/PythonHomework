# сделать поиск от ^ вправо если () или до знака
split = ('^', '/', '*', '%', '-', '+', '=', '<', '>', '!',  '(', ')', ',')
xprstr = 'e^(-e)^(-e+(2-3))'
print(xprstr)
left = xprstr.rindex('^')
skob = 0
print(xprstr[left:])
for j, data in enumerate(xprstr[left+1:]):
    if data  == '(':
        skob = skob + 1
    if data == ')':
        skob = skob - 1
    if data in split and data != '(' and skob == 0:
        break
    print(j, data, skob)

print('===', xprstr[left+1:left+2+j])
