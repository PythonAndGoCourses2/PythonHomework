from constants import *


def parse(expression):
    """This function get expression. Return the list of parsed arguments. """
    number, func, op = '', '', ''
    parsed_formula = []
    i = 0  # Символ строки
    while i < len(expression):
        symbol = expression[i]
        if expression[i].isalpha():
            func += symbol
        elif func in MATH_FUNC:
            while expression[i] != "(":  # For such function as log2, log10, etc
                func += expression[i]
                i += 1
            brackets = 1
            func_expr = ""  # Expression under function
            i += 1
            while brackets != 0:
                if expression[i] == '(':
                    brackets += 1
                elif expression[i] == ')':
                    brackets -= 1
                func_expr += expression[i]
                i += 1
            parsed_formula.append(float(math_function_calculating(MATH_FUNC[func], func_expr)))
            continue  # Because changed i value
        if expression[i].isdigit() or expression[i] == '.':
            number += symbol
        elif number:
            parsed_formula.append(float(number))
            number = ''

        if expression[i] in OPERATORS:
            op += expression[i]
        elif op:
            parsed_formula.append(op)
            op = ''

        if expression[i] in "()":
            parsed_formula.append(expression[i])
        i += 1
    if number:
        parsed_formula.append(float(number))
    return parsed_formula


def math_function_calculating(function, func_expr):
    """Take function and string expression under function."""
    list_of_arg = []
    argument, start_pos = 0, 0
    while argument != -1:
        argument = func_expr.find(",", start_pos)
        temp = func_expr[start_pos:argument]
        temp = calculating(temp)
        list_of_arg.append(temp)
        start_pos = argument + 1
    return function(*list_of_arg)


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
