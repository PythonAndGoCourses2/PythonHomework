from constants import *


def parse(expression):
    """This function get expression. Return the list of parsed arguments. """
    number, func, op, first_argument, second_argument = '', '', '', '', ''
    parsed_formula = []
    brackets = 0  # Счётчик скобок для функций
    i = 0  # Символ строки
    while i < len(expression):
        symbol = expression[i]
        if symbol.isalpha():
            func += symbol
        elif func in MATH_FUNC:
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
            op += symbol
        elif op:
            parsed_formula.append(op)
            op = ''

        if symbol in "()":
            parsed_formula.append(symbol)
        i += 1
    if number:
        parsed_formula.append(float(number))
    return parsed_formula


def infix_to_postfix(parsed_formula):
    """This function translate infix form into postfix form."""
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
    """Gets the list of arguments written in the reverse polish notation.
    Return calculated value.

    """
    stack = []
    for item in polish_notation:
        if item in OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(OPERATORS[item][1](x, y))
        else:
            stack.append(item)
    return stack[0]


def calculating(expression):
    """Parse expression and return calculated value."""
    return calc(infix_to_postfix(parse(expression)))
