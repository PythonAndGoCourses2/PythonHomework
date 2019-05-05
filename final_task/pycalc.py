import math
import argparse
import operator

OPERATORS = {'+': (1, operator.add),  # Первый элемент кортежа - приоритет
             '-': (1, operator.sub),  # Второй элемент - операция
             '*': (2, operator.mul),
             '/': (2, operator.truediv),
             '//': (2, operator.floordiv),
             '%': (2, operator.mod),
             '^': (3, operator.pow)}
math_const = {'e': math.e,
              'pi': math.pi}
math_function = dict([(attr, getattr(math, attr)) for attr in dir(math) if getattr(math, attr)])
math_function["abs"], math_function["round"] = abs, round  # Добавляем 2 built-in функции


def parse(expression):
    number, func, op, first_argument, second_argument = '', '', '', '', ''
    parsed_formula = []
    brackets = 0  # Счётчик скобок для функций
    i = 0  # Символ строки
    while i < len(expression):
        symbol = expression[i]
        if symbol.isalpha():
            func += symbol
        elif func in math_const:  # Если является мат. const
            parsed_formula.append(math_const[func])
            func = ''
        elif func in math_function:  # Если является мат. функцией
            while expression[i] != '(':  # То что до скобок определяем как второй аргумент
                second_argument += expression[i]
                i += 1
            else:
                first_argument += expression[i]  # Заносим "(" скобочку
                brackets += 1
                i += 1
            while brackets != 0:
                first_argument += expression[i]  # Заносим значение, которое находится внутри функции вместе с ")"
                if expression[i] == '(':  # Проверка на скобки
                    brackets += 1
                elif expression[i] == ')':
                    brackets -= 1
                if expression[i] == ',':
                    second_argument+=expression[i:]
                i += 1
            if not second_argument:
                parsed_formula.append(math_function[func](calculating(first_argument)))
            else:
                parsed_formula.append(math_function[func](calculating(first_argument), calculating(second_argument)))
            func = ''
            continue
        if symbol.isdigit() or symbol == '.':
            number += symbol
        elif number:
            parsed_formula.append(float(number))
            number = ''

        if symbol in OPERATORS:
            op += symbol
        elif op:
            parsed_formula.append(op)
            op = ''

        if symbol in "()":
            parsed_formula.append(symbol)
        i += 1

    if number:
        parsed_formula.append(float(number))
    elif func in math_const:
        parsed_formula.append(math_const[func])
    return parsed_formula


def infix_to_postfix(parsed_formula):
    """This function translate infix form into postfix form"""
    polish_notation, stack = [], []
    for item in parsed_formula:
        if item == '^':
            while stack and stack[-1] != '(' and OPERATORS[item][0] < OPERATORS[stack[-1]][0]:
                polish_notation.append(stack.pop())
            stack.append(item)
        elif item in OPERATORS:
            while stack and stack[-1] != '(' and OPERATORS[item][0] <= OPERATORS[stack[-1]][0]:
                polish_notation.append(stack.pop())
            stack.append(item)
        elif item == ')':
            while stack:
                x = stack.pop()
                if x == '(':
                    break
                polish_notation.append(x)
        elif item == "(":
            stack.append(item)
        else:  # Если число
            polish_notation.append(item)
    while stack:
        polish_notation.append(stack.pop())
    return polish_notation


def calc(polish_notation):
    stack = []
    for item in polish_notation:
        if item in OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(OPERATORS[item][1](x, y))
        else:
            stack.append(item)
    return stack[0]


def calculating(expression):
    return calc(infix_to_postfix(parse(expression)))


def main():
    print(calculating(create_parser().EXPRESSION))
    # print(calculating("2+3"))


def create_parser():
    parser = argparse.ArgumentParser(prog='pycalc', description="Pure-python command-line calculator.")
    parser.add_argument('EXPRESSION', help='expression string to evaluate', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    main()
