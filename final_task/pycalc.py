import math
import argparse
import operator
import check
from pprint import pprint

OPERATORS = {'+': (1, operator.add),  # Первый элемент кортежа - приоритет
             '-': (1, operator.sub),  # Второй элемент - операция
             '*': (2, operator.mul),
             '/': (2, operator.truediv),
             '//': (2, operator.floordiv),
             '%': (2, operator.mod),
             '^': (3, operator.pow)}
MATH_FUNC, MATH_CONST = {}, {}
MATH_FUNC["abs"], MATH_FUNC["round"] = abs, round  # Добавляем 2 built-in функции
for attr in dir(math):
    if type(getattr(math, attr)) != float:
        if callable(getattr(math, attr)):
            MATH_FUNC[attr] = getattr(math, attr)
    else:
        MATH_CONST[attr] = getattr(math, attr)
def parse(expression):
    number, func, op, first_argument, second_argument = '', '', '', '', ''
    parsed_formula = []
    brackets = 0  # Счётчик скобок для функций
    i = 0  # Символ строки
    while i < len(expression):
        symbol = expression[i]
        if symbol.isalpha():
            func += symbol
        elif func in MATH_FUNC:  # Если является мат. функцией
            while expression[i] != '(':  # Для таких функций как log10,log2 и т.д.
                func += expression[i]
                i += 1
            brackets += 1
            temp_string = expression[i]
            i += 1
            while brackets != 0:
                if expression[i] == '(':
                    brackets += 1
                elif expression[i] == ')':
                    brackets -= 1
                temp_string += expression[i]
                i += 1
            j = 1
            if temp_string.count(",") > 1:  # Если много параметров
                break
            temp_func = ''
            while j < len(temp_string) - 1:
                first_argument += temp_string[j]
                j += 1
                if temp_string[j].isalpha():
                    temp_func += temp_string[j]
                elif temp_func in MATH_FUNC:
                    while temp_string[j] != '(':  # Для таких функций как log10,log2 и т.д.
                        temp_func += temp_string[j]
                        first_argument += temp_string[j]
                        j += 1
                    temp_brackets = 1
                    first_argument += temp_string[j]
                    j += 1
                    while temp_brackets != 0:
                        first_argument += temp_string[j]
                        if temp_string[j] == '(':
                            temp_brackets += 1
                        elif temp_string[j] == ')':
                            temp_brackets -= 1
                        j += 1
                if temp_string[j] == ',':
                    second_argument += temp_string[j + 1:-1]
                    break

            if not second_argument:
                parsed_formula.append(MATH_FUNC[func](calculating(first_argument)))
            else:
                parsed_formula.append(MATH_FUNC[func](calculating(first_argument), calculating(second_argument)))
            func, first_argument, second_argument = '', '', ''
            continue
        if symbol.isdigit() or symbol == '.':
            number += symbol
        elif number:
            parsed_formula.append(float(number))
            number = ''

        if symbol in OPERATORS:
            if not op or symbol == '/':
                op += symbol
            else:
                number += symbol
                func += symbol
        elif op:
            parsed_formula.append(op)
            op = ''

        if symbol in "()":
            parsed_formula.append(symbol)
        i += 1
    if number:
        parsed_formula.append(float(number))
    elif func in MATH_CONST:
        parsed_formula.append(MATH_CONST[func])
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
    try:  # WIP(Обрабатывает не все типы исключений)
        expression = create_parser().expr
        comparison = check.comparison_check(expression)  # Определяем подаётся ли# строка на сравнение
        expression = check.correct_check(expression)  # Если всё нормально - возвращает строку
        expression = check.replace_whitespace_and_const(expression)
        expression = check.fix_unary(expression)
        expression = check.replace_plus_minus(expression)
        if expression:
            if not comparison:
                if check.brackets_check(expression):
                    print(calculating(expression))
            else:
                print(check.comparison_calc(expression, comparison))
        else:
            print("ERROR: no symbols to calculate")
    except ZeroDivisionError:
        print("ERROR: division by zero")
    except Exception:
        print("ERROR: incorrect expression")


def create_parser():
    parser = argparse.ArgumentParser(prog='pycalc', description="Pure-python command-line calculator.")
    parser.add_argument('expr', metavar='EXPRESSION', help='expression string to evaluate', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    main()
