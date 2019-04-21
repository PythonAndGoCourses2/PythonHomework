#!python
import argparse
import re
import string


def input_check(func):
    def wrapper():
        try:
            func()
            return func
        except SystemExit:
            print("ERROR string not recognized")
            quit()
        except RuntimeError as err:
            print("ERROR: in execute_rpn " + str(err.args[0]))
            quit()
        except ValueError:
            print("ERROR: in execute_rpn Unknown operand!")
            quit()
        except Exception:
            print("ERROR: in execute_rpn Unknown error!")
            quit()
    return wrapper()


@input_check
def create_arg_parser():
    global line
    pars = argparse.ArgumentParser(prog='pycalc', description='Pure-python command-line calculator.')
    pars.add_argument("EXPRESSION", type=str, help="expression string to evaluate")
    pars.add_argument('-m', '--use-module', metavar='MODULE', type=str, nargs='+',
                          help='additional user modules')
    args = pars.parse_args()
    line = args.EXPRESSION


create_arg_parser()


OPERATORS = {'>': (0, lambda x, y: x > y), "<": (0, lambda a, b: a < b),
             '>=': (0, lambda x, y: x >= y), "<=": (0, lambda a, b: a <= b),
             "==": (0, lambda a, b: a == b),
             '+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y),
             '%': (2, lambda x, y: x % y), "^": (3, lambda a, b: a ** b)
             }

z = 0
numbers = string.digits + '.'
mat = ('+', '-', '/', '*', '//', '**', '^', '%', '=')
letters = string.ascii_letters
result = 0


def split_operators(s):
    try:
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
    except Exception:
        print('fail func split_operators')


def matched(lines):
    try:
        count = 0
        for i in lines:
            if i == "(":
                count += 1
            elif i == ")":
                count -= 1
        if not int(count) == 0:
            print('ERROR: the number of open and closed brackets is not equal')
            quit()
    except Exception:
        print('fail func matched')


matched(line)


def only_letters(tested_string):
    try:
        check_in_mat = 0
        check_in_numbers = 0
        for sign in tested_string:
            if sign not in letters:
                continue
            else:
                print("ERROR: In the entered expression are not only numbers and math.")
                quit()
        if tested_string in mat:
            check_in_mat = 1
        if tested_string in numbers:
            check_in_numbers = 1
        if not check_in_mat == check_in_numbers:
            print("ERROR: wrong data")
            quit()
    except Exception:
        print('fail func only_letters')


only_letters(line)


def check_line(oneline):
    if oneline == ():
        print('ERROR: string None ')
        quit()
    elif oneline[-1] in mat:
        print('ERROR: The last value cannot be early ' + oneline[-1])
        quit()
    elif oneline[0] == ')':
        print('ERROR: The first value cannot be early ' + oneline[0])
        quit()
    elif oneline[-1] == '(':
        print('ERROR: The last value cannot be early ' + oneline[-1])
        quit()
    elif oneline[0] == '-':
        line.insert(0, '0')


line = split_operators(line)

check_line(line)

line = "".join(str(item) for item in line)


def sign_replacement(text):
    global line

    patterns_and_replacements = [
        (r" ", r""),
        (r"--", r"+"),
        (r"\++\+", r"+"),
        (r"\+-", r"-"),
        (r"-\+", r"-"),
        (r"\)\(", r")*("),
        (r"\(\+", r"("),
        (r"\(\-", r"(0-")
    ]

    check = True
    while check:
        check = False
        for item in patterns_and_replacements:
            text = re.sub(item[0], item[1], text)
        for item in patterns_and_replacements:
            if re.search(item[0], text):
                check = True
                break

    line = text


sign_replacement(line)

line = split_operators(line)

for idx, stack in enumerate(line):
    if stack == '(':
        if idx == 0:
            continue
        elif line[idx - 1] in mat:
            continue
        elif line[idx - 1] in numbers or line[idx - 1] == stack:
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
            place_star = idx + 1
            line.insert(place_star, '*')
            continue
        elif line[idx + 1] == stack:
            continue
        else:
            continue

line = "".join(str(item) for item in line)


def check_star(check_line):
    check = True
    global line
    while check:
        for idx, stack in enumerate(check_line):
            if stack == '*':
                if check_line[idx + 1] == stack:
                    x = check_line[idx - 1]
                    x_ind = idx - 1
                    y = check_line[idx + 2]
                    y_ind = idx + 2
                    if y == stack:
                        print('ERROR: not known mathematical action ***')
                        quit()
                    else:
                        z = int(x) ** int(y)
                        check_line = split_operators(check_line)
                        check_line[x_ind:y_ind + 1] = [z]
                        check_line = "".join(str(item) for item in check_line)
                        check = False
                        if re.search(r"\*\*", check_line):
                            check = True
                            check_star(check_line)
                            break
                elif check_line[idx + 1] != stack:
                    continue
        check = False
    line = "".join(str(item) for item in check_line)


check_star(line)

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
                line[x_ind:y_ind + 1] = [z]
                break
        elif line[idx + 1] != stack:
            continue

line = "".join(str(item) for item in line)


def eval_(formula):
    def parse(formula_string):
        try:
            number = ''
            for s in formula_string:
                if s in numbers:
                    number += s
                elif number:
                    yield float(number)
                    number = ''
                if s in OPERATORS or s in "()":
                    yield s
            if number:
                yield float(number)
        except Exception:
            print('fail func eval_parse')

    def shunting_yard(parsed_formula):
        try:
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
        except Exception:
            print('fail func eval_shunting')

    def calc(polish):
        try:
            stock = []
            for token in polish:
                if token in OPERATORS:
                    y, x = stock.pop(), stock.pop()
                    if y == 0 and token == '/':
                        print('ERROR: 0 cannot be divided')
                        quit()
                    else:
                        stock.append(OPERATORS[token][1](x, y))
                else:
                    stock.append(token)
            return stock[0]
        except Exception:
            print('fail func eval_calc')

    final_result = calc(shunting_yard(parse(formula)))
    if formula.find("!=") == -1:
        if formula.find("==") == -1:
            pass
        else:
            equality_index = formula.split('==')[0]
            if equality_index == '':
                final_result = calc(shunting_yard(parse(formula.split("==")[-1])))
            else:
                x_result = calc(shunting_yard(parse(formula.split("==")[0])))
                y_result = calc(shunting_yard(parse(formula.split("==")[-1])))
                print(x_result == y_result)
                exit(0)
        print(final_result)
    else:
        x_result = calc(shunting_yard(parse(formula.split("!=")[0])))
        y_result = calc(shunting_yard(parse(formula.split("!=")[-1])))
        print(x_result != y_result)


def start_calc(inp_line):
    eval_(inp_line)


start_calc(line)
