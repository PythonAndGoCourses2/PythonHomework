#!python
import argparse


def createArgParser():
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', type=str, help='expression string to evalute')
    parser.add_argument('-m', '--MODULE', type=str, help='use modules MODULE [MODULE...] additional modules to use')
    return parser


parser = createArgParser()
line = parser.parse_args().EXPRESSION


OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y),
             '%': (3, lambda x, y: x % y)}


z = 0
numbers = "0123456789."
mat = ('+', '-', '/', '*', '//', '**', '^', '%')
letters = "abcdefghjklmnopqrstuvwxyz &$#@абвгдежзиклмнопрстухцчюшщуыывюяё"
result = 0


def matched(str):
    count = 0
    for i in str:
        if i == "(":
            count += 1
        elif i == ")":
            count -= 1
        if count < 0:
            print('ERROR: opening bracket not found')
            quit()
    return count == 0


matched(line)


def only_letters(tested_string):
    for sign in tested_string:
        if sign not in letters:
            continue
        else:
            print("ERROR: In the entered expression are not only numbers and math.")
            quit()


only_letters(line)


if line[0] in mat:
    print('ERROR: The first value cannot be early ' + line[0])
    quit()
if line[-1] in mat:
    print('ERROR: The last value cannot be early ' + line[-1])
    quit()
if line[0] == ')':
    print('ERROR: The first value cannot be early ' + line[0])
    quit()
if line[-1] == '(':
    print('ERROR: The last value cannot be early ' + line[-1])
    quit()


for bracket in line:
    if bracket == '(':
        x = line.index('(')
        y = line[x + 1]
        if y in mat:
            print('ERROR: after the sign ( must be a number')
            quit()
        elif line.find(')') == -1:
            print('ERROR: a character was entered \'(\' but the character was not entered \')\'')
            quit()
        else:
            continue


if set(line).isdisjoint(mat):
    print('ERROR: The entered expression does not contain mathematical operations.')
    quit()


def split_operators(s):
    doker = []
    last_number = ""
    for c in s:
        if c in numbers:
            last_number += c
        else:
            if last_number:
                doker.append(last_number)
                last_number = ""
            if c:
                doker.append(c)
    if last_number:
        doker.append(last_number)
    return doker


line = split_operators(line)


for idx, stack in enumerate(line):
    if stack == '(':
        if idx == 0:
            continue
        elif line[idx - 1] in mat:
            continue
        elif line[idx - 1] in numbers or line[idx - 1] == stack:
            inpt_star = idx - 1
            line.insert(idx, '*')
            continue
        else:
            continue
    elif stack == ')':
        out = len(line)
        if idx == out - 1:
            break
        elif line[idx + 1] in mat:
            continue
        elif line[idx + 1] in numbers or line[idx + 1] == '(':
            inpt_star = idx + 1
            line.insert(inpt_star, '*')
            continue
        elif line[idx + 1] == stack:
            continue
        else:
            continue


line = "".join(str(item) for item in line)


for idx, stack in enumerate(line):
    if stack == '*':
        if line[idx + 1] == stack:
            x = line[idx - 1]
            x_ind = idx - 1
            y = line[idx + 2]
            y_ind = idx + 2
            if y == stack:
                print('ERROR: not known mathematical action ***')
                quit()
            elif y in mat:
                print('ERROR: not known mathematical action **' + y)
                quit()
            else:
                z = int(x) ** int(y)
                line = split_operators(line)
                line[x_ind:y_ind+1] = [z]
                break
        elif line[idx + 1] != stack:
            continue


line = "".join(str(item) for item in line)


for idx, stack in enumerate(line):
    if stack == '/':
        if line[idx + 1] == stack:
            x = line[idx - 1]
            x_ind = idx - 1
            y = line[idx + 2]
            y_ind = idx + 2
            if y == stack:
                print('ERROR: not known mathematical action ///')
                quit()
            else:
                z = int(x) // int(y)
                line = split_operators(line)
                line[x_ind:y_ind+1] = [z]
                break
        elif line[idx + 1] != stack:
            continue


line = "".join(str(item) for item in line)


def eval_(formula):
    def parse(formula_string):
        number = ''
        for s in formula_string:
            if s in '1234567890.':
                number += s
            elif number:
                yield float(number)
                number = ''
            if s in OPERATORS or s in "()":
                yield s
        if number:
            yield float(number)

    def shunting_yard(parsed_formula):
        stack = []
        for token in parsed_formula:
            if token in OPERATORS:
                while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            elif token == '**':
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(polish):
        stack = []
        for token in polish:
            if token in OPERATORS:
                y, x = stack.pop(), stack.pop()
                if y == 0 and token == '/':
                    print('ERROR: 0 cannot be divided')
                    quit()
                else:
                    stack.append(OPERATORS[token][1](x, y))
            else:
                stack.append(token)
        return stack[0]

    final_result = calc(shunting_yard(parse(formula)))
    print(final_result)
#    return final_result


def start_calc(inp_line):
    eval_(inp_line)


start_calc(line)
